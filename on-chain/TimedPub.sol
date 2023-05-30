// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

import "./EllipticCurve.sol";

contract TaskSC{
    using EllipticCurve for *;

    //use these for printing in remix when using local node.
    event result_instance(bytes, bool, uint);

    event result_bool(bool a);

    event result_string(string a);

    event result_multi(bytes a, uint a_bitlen, bytes b, uint b_bitlen, bytes c, uint c_bitlen);

    // y^2 = x^3 + ax + b (mod p)
    uint256 p = 0xffffffffffffffffffffffffffffffff000000000000000000000001;
    uint256 gx = 0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21;
    uint256 gy = 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34;
    uint256 n_ec = 0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d;
    uint256 a = 0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe;
    uint256 b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4;


    constructor() payable {}

    struct Sender{
        address Adds;
        uint256[] alphax;
        uint256[] alphay;
        uint tfStart;
        uint tfEnd;
        uint salary;
        uint IDt;
        uint payment;
        uint deposit;
        uint count;
        string[] Proof;
    }
    struct Mailman{
        address MailmenAdd;
        bool invoker;
        uint M;
        uint index;
        uint salary;
    }
    struct S{
        uint IDt;
        uint256[] Sx;
        uint256[] Sy;
    }

    event Init (uint index);



    uint public i=0;


    function InitPara() external{
        emit Init(i);
    }

    event Published(
        address sender,
        uint IDt);

    mapping(uint=>S) public s;
    mapping(uint=>Sender) public senders;
    mapping(uint=>mapping(uint=>Mailman)) public mailmen;


    function PubTask(
        address _Adds,
        uint256[] memory _alphax,
        uint256[] memory _alphay,
        uint _tfStart,uint _tfEnd,
        uint _payment,uint _n,
        string[] memory _Proof
    )
    payable public returns(uint)
    {
        senders[i]=Sender({
        Adds:_Adds,
        alphax:_alphax,
        alphay:_alphay,
        tfStart:_tfStart,
        tfEnd:_tfEnd,
        salary:_payment/_n,
        IDt:i,
        payment:_payment,
        deposit:0,
        count:0,
        Proof:_Proof
        });

        uint IDt=i;
        i++;
        emit Published(
            senders[IDt].Adds,
            senders[IDt].IDt);
        return IDt;
    }

    event Registed(uint index);


    function Register (uint _IDt,uint _deposit,uint _n) public payable returns (uint){
        if(senders[_IDt].count<_n && mailmen[i][senders[_IDt].count].invoker==false){
            uint _count=++senders[_IDt].count;
            mailmen[_IDt][_count]=Mailman({
            MailmenAdd: msg.sender,
            invoker: true,
            M: _deposit,
            index: _count,
            salary: 0
            });

            payable(address(this)).transfer(_deposit);
            senders[_IDt].deposit+=_deposit;
            emit Registed(_count);
            return _count;
        }
        else{
            return 0;
        }
    }

    function Shares (uint256[] memory _Sx, uint256[] memory _Sy, uint _IDt, uint _n) external {
        s[_IDt]=S({
        IDt:_IDt,
        Sx:_Sx,
        Sy:_Sy
        });
    }

    function PubShare(uint _IDt,uint _index,uint256 _ss,uint _n,uint _pt)  public payable{
        uint256 _Sx = s[_IDt].Sx[_index-1];
        uint256 _Sy = s[_IDt].Sy[_index-1];
        (uint256 SSx, uint256 SSy) = EllipticCurve.ecMul(_ss, gx, gy, a, p);

        uint salary=address(this).balance/_n;
        if( _Sx==SSx && _Sy==SSy && _pt>senders[_IDt].tfStart && _pt<senders[_IDt].tfEnd){
            payable(msg.sender).transfer(salary);
            senders[_IDt].payment-=salary;
        }
    }

    function Report(uint _IDt,uint _n, uint _index,uint256[] memory _DL,uint _pt) public payable{

        uint256 c = uint256(bytes32(sha256(abi.encodePacked(s[_IDt].Sx[_index-1]+s[_IDt].Sy[_index-1]+_DL[0]+_DL[1]+_DL[3]))));
        (uint256 tmpx, uint256 tmpy) = EllipticCurve.ecMul(c, s[_IDt].Sx[_index-1], s[_IDt].Sy[_index-1], a, p);
        (uint256 leftx, uint256 lefty) = EllipticCurve.ecAdd(_DL[0], _DL[1], tmpx, tmpy, a, p);
        (uint256 rightx, uint256 righty) = EllipticCurve.ecMul(_DL[2], gx, gy, a, p);


        uint salary=address(this).balance/_n;

        if( leftx==rightx && lefty==righty && _pt>senders[_IDt].tfStart && _pt<senders[_IDt].tfEnd){
            payable(msg.sender).transfer(salary);
            senders[_IDt].payment-=salary;
        }
    }

    function Refund(uint _IDt,uint _n,uint _pt)public payable{
        if(_pt>senders[_IDt].tfStart){
            payable(msg.sender).transfer(senders[_IDt].payment);


            for(uint k=0;k<_n;k++){
                uint index=mailmen[_IDt][k].index;
                if(mailmen[_IDt][index-1].M != 0){
                    payable(msg.sender).transfer(mailmen[_IDt][index-1].M);
                }
            }


        }

    }

    receive() external payable {
    }
    fallback() external payable {
    }

}