# expenseManagementSystem

 a simple expense management system that provides RESTful endpoints for CRUD operations using python flask.

#Objective 
 Use Python Flask to develop REST API. Perform basic expense application which performs GET, PUT, POST, DELETE operations.
 
 -Implemented round robin load balancing for traffic distribution which eliminates overloading of a single replica instance.
 -Implemented Redis routing table which routes requests to available replica instances and maintains it for upcoming requests.
 -Achieved quick failure detection by implementing circuit breaker, preventing routing requests to failed replica instances.
 -Implemented sharding using consistent hashing (configurable to use HRW/Rendezvous hashing) which improves scalability.
 -Achieved fault tolerance by implementing active replication of docker instances which increases availability.

