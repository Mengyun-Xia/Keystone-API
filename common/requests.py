# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import curlify
import requests
import json
import hashlib
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.logUtils import logger
#from helper.logoperator import logger
#from helper.public import Public
#from helper.qciurl import QciUrl

class Author(object):
    #baseURI = Public.read_yaml('domain')
    #current_team = Public.read_yaml('team')
    #user_email = Public.read_yaml('user')
    #password = Public.read_yaml('password')

    def __init__(self):
        self.headers = {"Content-Type": "application/json;charset=utf-8"}
        self.project_name = None
        self.project_id = None
        self.docker_repo = None
        self.maven_repo = None

    def get(self, url, body=None) -> json:
        if not isinstance(body, dict):
            logger.error("当前请求体类型: {},应为: {}".format(type(body), "dict"))
            return "入参类型有误"

        response = requests.get(
            Author.baseURI + "/api" + url,
            params=body,
            headers=self.__getattribute__("headers"),
            cookies=self.__getattribute__("cookies")
        )
        logger.info(curlify.to_curl(response.request))

        try:
            return response.json()
        except:
            raise response.raise_for_status()

    def post(self, url, body=None, params=None, header=0) -> json:
        if not isinstance(body or params, dict):
            logger.error("当前请求体类型: {},应为: {}".format(type(body), "dict"))
            return "入参类型有误"
        
        if header == 1:
            self.headers["Content-Type"] = "application/x-www-form-urlencoded;charset=utf-8"
            body = body
        else:
            self.headers["Content-Type"] = "application/json;charset=utf-8"
            body = json.dumps(body)
        response = requests.post(
            Author.baseURI + "/api" + url,
            data=body,
            params=params,
            headers=self.__getattribute__("headers"),
            cookies=self.__getattribute__("cookies")
        )
        logger.info(curlify.to_curl(response.request))

        try:
            return response.json()
        except:
            raise response.raise_for_status()

    def patch(self, url, body=None, params=None, header=0) -> json:
        if not isinstance(body or params, dict):
            logger.error("当前请求体类型: {},应为: {}".format(type(body), "dict"))
            return "入参类型有误"

        if header == 1:
            self.headers["Content-Type"] = "application/x-www-form-urlencoded;charset=utf-8"
            body = body
        else:
            self.headers["Content-Type"] = "application/json;charset=utf-8"
            body = json.dumps(body)
        response = requests.patch(
            Author.baseURI + "/api" + url,
            data=body,
            params=params,
            headers=self.__getattribute__("headers"),
            cookies=self.__getattribute__("cookies")
        )
        logger.info(curlify.to_curl(response.request))

        try:
            return response.json()
        except:
            raise response.raise_for_status()

    def put(self, url, body=None, params=None, header=0) -> json:
        if not isinstance(body or params, dict):
            logger.error("当前请求体类型: {},应为: {}".format(type(body), "dict"))
            return "入参类型有误"

        if header == 1:
            self.headers["Content-Type"] = "application/x-www-form-urlencoded;charset=utf-8"
            body = body
        else:
            self.headers["Content-Type"] = "application/json;charset=utf-8"
            body = json.dumps(body)
        response = requests.put(
            Author.baseURI + "/api" + url,
            data=body,
            params=params,
            headers=self.__getattribute__("headers"),
            cookies=self.__getattribute__("cookies")
        )
        logger.info(curlify.to_curl(response.request))

        try:
            return response.json()
        except:
            raise response.raise_for_status()

    def delete(self, url, body=None) -> json:
        if not isinstance(body, dict):
            logger.error("当前请求体类型: {},应为: {}".format(type(body), "dict"))
            return "入参类型有误"

        response = requests.delete(
            Author.baseURI + "/api" + url,
            params=body,
            headers=self.__getattribute__("headers"),
            cookies=self.__getattribute__("cookies")
        )
        logger.info(curlify.to_curl(response.request))

        try:
            return response.json()
        except:
            raise response.raise_for_status()

    def add_header(self, key, value) -> json:
        if not hasattr(self, key):
            self.headers.update({key: value})

        return self

    @staticmethod
    def get_user_password(password):
        """
        sha1 加密
        """
        if type(password) is not str:
            password = str(password)
        return hashlib.sha1(password.encode('utf-8')).hexdigest()

    def login(self):
        if Public.read_yaml('cookies') is None:
            login_url = Author.baseURI + "/api/v2/account/login"
            body = {"account": Author.user_email, "password": Author.get_user_password(Author.password)}
            login_response = requests.post(login_url, data=body)
            logger.info("login：{}".format(login_response.json()))
            xsrf_token = requests.utils.dict_from_cookiejar(login_response.cookies).get("XSRF-TOKEN")
            self.add_header("X-XSRF-TOKEN", xsrf_token)
            self.__setattr__("cookies", requests.utils.dict_from_cookiejar(login_response.cookies))
        else:
            self.add_header("X-XSRF-TOKEN", Public.read_yaml('xsrf-token'))
            self.__setattr__("cookies", Public.read_yaml('cookies'))

        return self

    def createProject(self):
        if Public.read_yaml('projectname') is None:
            self.project_name = "ci_api_" + Public.random_str()
            params = {
                "name": self.project_name,
                "displayName": self.project_name,
                "description": "qci 自动化创建的项目",
                "projectTemplate": "DEV_OPS",
                "icon": "/static/project_icon/scenery-version-2-6.svg"
            }
            response = self.post(QciUrl.create_project_URI(), body=params, header=1)
            logger.info("创建项目: {}".format(response))
        else:
            self.project_name = Public.read_yaml('projectname')

    def getProjectId(self):
        pamars = {"page": 1, "pageSize": 30,
                  #"groupId": 1,
                  "keyword": self.project_name, "type": "JOINED",
                  "archived": False, "sort": "VISIT", "order": "DESC"
                  }
        response = self.get(QciUrl.get_project_id(), body=pamars)
        self.project_id = str(response.get("data").get("list")[0].get("id"))
        self.add_header("X-Project-Id", self.project_id)

    def createArtiactsRepo(self):
        docker_name = "docrepo"
        maven_name = "mvnrepo"
        # type 1 generic, 2 docker, 3 maven
        body = {"name": docker_name, "description": "", "accessLevel": 1, "type": 2, "allowProxy": True}
        resp = self.post(QciUrl.create_artifacts_job(self.project_name), body=body)
        assert resp.get("msg") == "succeeded"
        body = {"name": maven_name, "description": "", "accessLevel": 1, "type": 3, "allowProxy": True}
        resp = self.post(QciUrl.create_artifacts_job(self.project_name), body=body)
        assert resp.get("msg") == "succeeded"
        self.docker_repo = docker_name
        self.maven_repo = maven_name

if __name__ == '__main__':
    au = Author()
    au.login()
    au.createProject()
    au.getProjectId()




