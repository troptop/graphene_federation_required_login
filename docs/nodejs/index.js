//const { ApolloServer } = require("apollo-server");
const { ApolloServer } = require("apollo-server-express");
const { ApolloGateway, RemoteGraphQLDataSource } = require("@apollo/gateway");
const express = require("express");
const cors = require("cors");
const mw_auth = require("./middleware.js");
const serviceE_url = "http://172.17.0.1:8001/evntz";
const serviceF_url = "http://172.17.0.1:8000/api";

const responseHeadersToForward = [
	// Forward any cookies that the backends set.
	"set-cookie",
];

class KhanDataSource extends RemoteGraphQLDataSource {
	willSendRequest({ request, context }) {
		context.req.headers["Gfrl-Federation-Header"] = JSON.stringify(
			context.user
		);
		request.http.headers = context.req.headers;
	}
	async process({ request, context }) {
		// `response` here is the response we got back from the backend.
		const response = await super.process({
			request,
			context,
		});
		//console.log(response);

		if (request.http.url == "http://172.17.0.1:8000/api") {
			responseHeadersToForward.forEach((name) => {
				if (response.http.headers.get(name) != null) {
					response.http.headers.raw()[name].forEach((value, key) => {
						context.res.append(name, value);
					});
				}
			});
		}
		return response;
	}
}

const gateway = new ApolloGateway({
	serviceList: [
		{ name: "service_API_EVNTZ", url: serviceE_url },
		{ name: "service_API_AUTH", url: serviceF_url },
	],
	buildService({ name, url }) {
		return new KhanDataSource({
			url,
		});
	},
});
const graphqlContext = async ({ req, res }) => {
	user = await mw_auth(req);
	//console.log(user);
	return { user: user, req, res };
	//return { req, res };
};
const server = new ApolloServer({
	gateway,
	context: graphqlContext,
	subscriptions: false,
	debug: false,
	playground: {
		settings: {
			"request.credentials": "include",
		},
	},
});
const app = express();
app.use(
	cors({
		origin: "http://localhost:3000",
		optionsSuccessStatus: 200,
		credentials: true,
	})
);

const path = "/";
server.applyMiddleware({ app, path });
app.listen({ port: 3000 }, () =>
	console.log(`🚀 Server ready at http://localhost:3000${server.graphqlPath}`)
);
