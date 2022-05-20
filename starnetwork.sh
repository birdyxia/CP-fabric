HLF_VERSION=1.4.6
docker pull hyperledger/fabric-peer:${HLF_VERSION}
docker pull hyperledger/fabric-orderer:${HLF_VERSION}
docker pull hyperledger/fabric-ca:${HLF_VERSION}
docker pull hyperledger/fabric-ccenv:${HLF_VERSION}
cd fabric-sdk-py/
docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls.yaml up