# DataUber

## Introduction

DataUber is a complaint-supported timed data delivery system based on blockchain. It supports a sender to deliver some data to a recipient in a preset time without being online at that time. This repo contains the implementation of a DataUber prototype.

- `./on-chain`: includes the implementation of the smart contract $\textit{TimedPub}$.
- `./off-chain`: includes the implementation of the interactions between the sender and mailmen.

## Dependencies

- Basic packages: 
  - Shamir-17.12.0
  - gmpy2-2.1.5
  - PyCryptodome-3.14.1
  - fastecdsa-2.3.0

The packages above can be directly installed via `pip install`. Note that, for fastecdsa, a C compiler is required.  [GMP](https://gmplib.org/) is also required as the underlying C code in this package includes the `gmp.h` header (and links against gmp via the `-lgmp` flag).

## Build & Usage

> Python version: 3.9
>
> We recommend Python 3 and the later versions for building the project

1. Deploy the smart contract $\textit{TimedPub}$. Users are recommended to use the online IDE [Remix](https://remix.ethereum.org) to deploy the smart contract. After choosing the underlying blockchain network and the account for deployment, users can use the source code included in ./on-chain to deploy $\textit{TimedPub}$ and obtain its address on the blockchain (Note that the BigNumber.sol is also a contract invoked by TimedPub.sol).
2. Other transactions such as applying and registration can be conducted using a wallet app such as [MetaMask](https://metamask.io/).
3. Preparing for off-chain test. Users should install python and all aforementioned packages before running corresponding source code.
4. The the off-chain interactions between the sender and mailmen can be tested. 
   - Run ./offchain/OVTSS.py 
