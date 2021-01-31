### **KIS – ERPNext**

**Installing – 2 options**

_choose one (1) option to install the kis:_

**Own Image:**

`docker pull alexandradorner/kis` to pull the docker image

`docker run -d - -name kis -p 80:80 alexandradorner/kis` to run the app


`--> localhost:8080` to try it out

`docker exec -it kis bash`  to get inside the container’s shell and to run bench commands

**ERPNext + Custom App:** (preferred)

`docker pull lukptr/ernext` to pull the docker image

`docker run -d - -name erpnext -p 81:80 lukptr` to run the app

`docker exec -it erpnext bash` to get inside the container’s shell and to run bench commands

`bench get-app https://github.com/alexdorner/diplomprojekt-byh` to get your custom app (kis)

`bench install-app kis` to install the kis

`--> localhost:8180` to try it out
