import cmlapi
import requests
import json
from cmlapi.rest import ApiException
import os

api_instance = cmlapi.default_client()
runtime_repo_file = 'http://cloudera-build-2-us-west-2.vpc.cloudera.com/s3/build/70673392/cloudera-ai-agent-studio/2.x/artifacts/repo-assembly.json'


def read_runtime_repo_file() -> str:
    try:
        response = requests.get(runtime_repo_file)
        response.raise_for_status() 
        data = response.json()
        image_identifier = data['runtimes'][0].get('image_identifier')
        print(image_identifier)

        return image_identifier
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the request: {e}")
        return ""
    except json.JSONDecodeError:
        print("Failed to decode JSON from the response.")
        return ""


def validate_and_register_runtime_image(image_identifier) -> bool:
    try:
        api_response = api_instance.validate_custom_runtime(url=image_identifier)
        data = api_response.to_dict()
        print(data)
        if data['success'] == True:
            if register_runtime_image(runtime_image) == True:
                print("Agent Studio runtime image is registered")
                return True
            else:
                print("Failed to register agent studio runtime image. Please contact support or system administrator")
                return False
        else:
            if data['reason'] == "duplicateRuntimeVersion":
                print("Agent studio runtime image is already registered")
                return True
            else:
                print("Failed to validate agent studio runtime image. Please contact support or system administrator")
                return False
    except ApiException as e:
        print("Exception when calling CMLServiceApi->validate_custom_runtime: %s\n" % e)
        return False

def register_runtime_image(image_identifier) -> bool:
    try:
        body = cmlapi.RegisterCustomRuntimeRequest()
        body.url = image_identifier
        api_response = api_instance.register_custom_runtime(body)
        print(api_response)
        return True
    except ApiException as e:
        print("Exception when calling CMLServiceApi->register_custom_runtime: %s\n" % e)
        return False

def create_agent_studio_application(image_identifier) -> bool:
    try:
        cmlapi.create_application(
            cmlapi.CreateApplicationRequest(
                name="Agent Studio",
                subdomain="cai-agent-studio",
                description="Agent Studio",
                script="run-app.py",
                cpu=4,
                memory=16,
                nvidia_gpu=0,
                bypass_authentication=True,
                runtime_identifier=image_identifier,
            ),
            project_id=os.environ.get("CDSW_PROJECT_ID"),
        )
        print("Agent Studio application started successfully")
        return True
    except Exception as e:
        print(f"Error creating application: {e}")
        return False


print("Adding agent studio runtime image to runtime catalog")
runtime_image = read_runtime_repo_file()
#For dev testing only
runtime_image = runtime_image.replace("docker.repository.cloudera.com","docker-private.infra.cloudera.com")
if runtime_image and runtime_image != "":
    if validate_and_register_runtime_image(runtime_image):
        create_agent_studio_application(runtime_image)
    else:
        print("Failed to validate and register agent studio runtime image")
else:
    print("Failed to read agent studio runtime image")