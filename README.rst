=====
Graphene Federation Required Login (GFRL)
=====

GFRL is a Django decorator for Graphene Federation authentication.
To use it you need to setup :
- Graphql Gateway (Apollo Federation https://www.apollographql.com/docs/apollo-server/federation/gateway/)
- Django Graphene Federation (https://github.com/preply/graphene-federation)
- Django Graphene (https://docs.graphene-python.org/projects/django/en/latest/)

Overview
-----------
                                      --------------------
                                      |      Client      |
                                      |     Front/App    |
                                      --------------------
                                                |
                                            [1] | [A]
                                            [5] | [E]
                                                |
                                      ---------------------
          NodeJS                      | Apollo Federation |
          Gateway                     |       Gateway     |
                                      ---------------------
                                        |  [4][Aa][B]   |    
                                    [2] | [Ab]          | [C]   
                                        |               |    
                        ----------------------       -------------------------
    Django Graphene     |      User Node     |       |       Post Node       |
    Backend Service     | User data and auth |       | (with GFRL decorator) |
                        ----------------------       -------------------------
                                 [3]                            [D]

Authentication Process
[1] Client/User send a request to Apollo Federation to Authenticate (username - password / socialAuth / jwt...)
[2] Apollo Federation redirect to User Node Service
[3] User Node Authenticate the user and return a session / token...
[4] Apollo Federation send the session / token back to the client
[5] session stored in the client browser / token received by the client

Get Posts Process
[A] Client/User send a request to Apollo Federation to get his Posts
[Aa][sub_request] Apollo Federation creates an internal request to check if the User is Authenticated 
by sending a request to the User Node with the header from the client request (token in the header or sessionID)
[Ab][sub_request] Apollo Federation received User information (id,name,email...) corresponding to the client Authencation information 
[B] Apollo server modify the header of the client request adding a new header with the User information it gets from the sub_request to the UserNode [Ab]
By Default it adds a header named "gfrl" with the data receive from the internal sub_request [Ab] 
[C] Apollo send the request to the Post Node with the User information in the header (by default header name is "gfrl")
[D] Posts Node inspect the header (looking for gfrl), and add it to info.context graphene parameter
If info.context.gfrl contains user information (id,email...), 
the Posts Node respond to Apollo Federation with the Posts corresponding to the User id
Else return an error of permission denied
[E] Apollo Federation responds to the client with the information received from the Posts Node


Quick start
-----------

1. Add "GFRL" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'graphene_federation_required_login',
    ]
2. Add GFRL middleware to the Graphene MIDDLEWARE

    GRAPHENE = {
        'MIDDLEWARE': (
            'graphene_federation_required_login.middleware.AuthorizationMiddleware',
        ),
}
3. Import the decorator in the file you need

    from graphene_federation_required_login.decorators import required_federation_login

4. You can use it for any function that contains the parameter "info.context" such as :
   - Query
        @required_federation_login
        def resolve_user_event(self, info, **kwargs):
            event = None
            id = info.context.gfrl['id']        
            event = types.UserType(id=id)
            return event
   - Mutation
        @required_federation_login  
        def mutate_and_get_payload(cls, root, info, name, **input):
            event = Event(name=name)
            return AddEvent(event=event)

Additional Parameters
-----------    

1. Add GFRL_DJANGO_CONTEXT in settings.py
    GFRL_DJANGO_CONTEXT is the name of the info.context attribute where the user information will be stored
    By default the attribute name "gfrl".
    You can access the user information through is info.context.gfrl. 

2. Add GFRL_FEDERATION_HEADER in settings.py
    GFRL_FEDERATION_HEADER is the name of the HTTP Header added by the Apollo federation gateway 
    where the user information will be stored to be sent to the django graphene service (Posts Node)
    By default the HTTP header name is 'Gfrl-Federation-Header'. (according to what you will develop in the Apollo federation gateway)
    !IMPORTANT! HTTP header only allow dash separated words. (underscore and space does not work)
    You can access the user information through is info.context.headers['Gfrl-Federation-Header']. 


Apollo Federation
----------------
I am sharing an example of Apollo Federation Gateway in the Docs folder.
more info https://www.apollographql.com/docs/apollo-server/federation/introduction/
