import subprocess, json, sys

secrets_to_validate = ["username", "password"];
env_vars_to_validate = ["serverBaseUrl", "inactivityTimeoutMinutes", "room"]

cmd_str = "flyctl secrets list -j"
result = subprocess.run(cmd_str, shell=True, capture_output=True, check=True)
json_out = json.loads(result.stdout);

validConfig = True

# check if the json_out array contains an object with key,value name,password and an object with key,value name,username
for secret_to_validate in secrets_to_validate:
    if not any(env_secret.get("Name") == secret_to_validate for env_secret in json_out):
        sys.stderr.write(f"{secret_to_validate} secret is missing\n")
        validConfig = False

cmd_str = "flyctl config show"
result = subprocess.run(cmd_str, shell=True, capture_output=True, check=True)
json_out = json.loads(result.stdout);

for env_var_to_validate in env_vars_to_validate:
    if not json_out.get("env").get(env_var_to_validate):
        sys.stderr.write(f"{env_var_to_validate} environment variable is missing\n")
        validConfig = False

if not validConfig:
    sys.stdout.write("Config not valid!\n")
    sys.exit(1)
else:
    sys.stdout.write("Config valid\n")
    sys.exit(0)
