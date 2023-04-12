FROM neo4j:4.4

RUN mkdir /scripts/

ADD ./scripts/init.cypher /scripts/
ADD ./scripts/schema.cypher /scripts/

RUN chmod 777 /scripts/*

# RUN echo "apoc.initializer.neo4j.1=CALL apoc.cypher.runSchemaFile(\"file:////scripts/schema.cypher\")" >> /conf/apoc.conf
# RUN echo "apoc.initializer.neo4j.2=CALL apoc.cypher.runFile(\"file:////scripts/init.cypher\")" >> /conf/apoc.conf