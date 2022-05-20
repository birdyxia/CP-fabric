# cd fabric-sdk-py/
# docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls.yaml up -d
# docker-compose -f test/fixtures/ca/docker-compose.yml up -d

cd fabric-sdk-py/workspace/
python3 testnetwork.py
python3 creat_connection.py
python3 connect_chaincode.py

cd /home/user/fabric/myproject
nohup python3 manage.py runserver 0.0.0.0:8000 &> server.log &

cd /home/user/fabric/fabric-sdk-py/workspace
python3 file.py

cd /home/user/fabric/fabric-sdk-py/workspace
python3 SGX.py