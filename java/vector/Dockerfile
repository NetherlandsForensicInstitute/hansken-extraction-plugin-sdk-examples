FROM openjdk:11.0.9.1-jre-buster

ADD target/*.tar.gz ./

EXPOSE 8999
ENTRYPOINT ["java", "-jar", "plugin.jar"]
