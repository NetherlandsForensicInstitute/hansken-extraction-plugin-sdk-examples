FROM eclipse-temurin:21.0.4_7-jre-noble

ADD target/*.tar.gz ./

EXPOSE 8999
ENTRYPOINT ["java", "-jar", "plugin.jar"]
