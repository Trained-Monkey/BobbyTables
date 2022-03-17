import os
import yaml

# Set up .env
with open('.env', 'w') as f:
    lines = ['MONGODB_USER=' + os.environ.get('MONGODB_USER'), 'MONBODB_PASSWORD=' + os.environ.get('MONBODB_PASSWORD'),
             'GC_SERVICE_ACC_PRIVATE_KEY_ID=' + os.environ.get('GC_SERVICE_ACC_PRIVATE_KEY_ID'),
             'GC_SERVICE_ACC_PRIVATE_KEY=' + os.environ.get('GC_SERVICE_ACC_PRIVATE_KEY'),
             'GC_SERVICE_ACC_CLIENT_EMAIL=' + os.environ.get('GC_SERVICE_ACC_CLIENT_EMAIL'),
             'GC_SERVICE_ACC_CLIENT_ID=' + os.environ.get('GC_SERVICE_ACC_CLIENT_ID')]
    f.writelines(lines)


# Reformat requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = f.readlines()
# Remove scrapy from requirements
requirements = requirements[1:]
with open('requirements.txt', 'w') as f:
    f.writelines(requirements)

# Set up scrapinghub.yml
with open('scrapinghub.yml', 'r') as f:
    d = yaml.load(f.read(), Loader=yaml.FullLoader)
    d['apikey'] = os.environ['ZYTE_API_KEY']

# update config to file
with open('scrapinghub.yml', 'w') as f:
    yaml.dump(d, f, default_flow_style=False)