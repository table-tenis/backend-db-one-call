## **BACKEND - DATABASE - ONE CALL**

### **Running Database Services And Kafka-To-Database Service**
- docker-compose -f docker-compose-mariadb up -d
- docker-compose -f docker-compose-redis up -d
- [Database Repository](http://172.21.100.253:3000/XFace/database)
- [Mariadb Wiki](http://172.21.100.253:3000/XFace/doc/wiki/MariaDB)
- Dump existed face data to database: 
```
cd python-scripts
python dump_facedata_db.py
```
- Consumer to database: 
```
cd python-scripts
python consumer_to_db.py
```

### **Running API Gateway And Services**
- docker-compose -f docker-compose-traefik up -d
- docker-compose -f docker-compose-account-service up -d
- docker-compose -f docker-compose-enterprise-service up -d
- docker-compose -f docker-compose-report-service up -d
- [API Gateway Repository](http://172.21.100.253:3000/XFace/api-gateway)
- [API Services Repository](http://172.21.100.253:3000/XFace/api-services)
- [Account, Access Management API Wiki](http://172.21.100.253:3000/XFace/doc/wiki/Access-Management)
- [Enterprise API Wiki](http://172.21.100.253:3000/XFace/doc/wiki/Enterprise-API)
- [Report API Wiki](http://172.21.100.253:3000/XFace/doc/wiki/Reporting)


### **Running All Service In One-Call**
- ./one-call.sh



