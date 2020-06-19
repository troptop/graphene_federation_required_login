const { createHttpLink } = require("apollo-link-http");
const { ApolloClient } = require("apollo-client");
const { InMemoryCache } = require("apollo-cache-inmemory");
const { gql } = require("apollo-server");
const fetch = require("node-fetch");
const { setContext } = require("apollo-link-context");

const mw_auth = async (req) => {
	if (req.originalUrl != "/.well-known/apollo/server-health") {
		const authLink = setContext((_, { headers }) => {
			return {
				headers: {
					...headers,
					...req.headers,
				},
			};
		});

		const httpLink = createHttpLink({
			uri: "http://172.17.0.1:8000/api",
			fetch: fetch,
		});
		const client = new ApolloClient({
			link: authLink.concat(httpLink),
			cache: new InMemoryCache(),
		});
		const MY_QUERY = gql`
			query {
				me {
					id
					email
				}
			}
		`;
		// a query with apollo-client
		const result = client.query({
			query: MY_QUERY,
		});
		return result.then((response) => response.data.me);
	}
};
module.exports = mw_auth;
