// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;


import "./BigNumber.sol";
contract TaskSC{
    using BigNumber for *;

    //use these for printing in remix when using local node.
    event result_instance(bytes, bool, uint);

    event result_bool(bool a);

    event result_string(string a);

    event result_multi(bytes a, uint a_bitlen, bytes b, uint b_bitlen, bytes c, uint c_bitlen);

    bytes g_val = "1249348110899368046253707745697105433416425539749";
    bytes q_val = "2006361285382876702406644607746542778541575996703";
    // bytes h_val = "1149156418779331981575308452978668258332815677736";
    // bool g_neg = false;
    // uint g_bitLen = 244;
    // bool h_neg = false;
    // uint h_bitLen =244;

    BigNumber.instance g = BigNumber.instance(g_val, false, 256);
    BigNumber.instance q = BigNumber.instance(q_val, false, 256);



    constructor() payable {}

    struct Sender{
        address Adds;
        string[] SSiHash;
        uint tfStart;
        uint tfEnd;
        uint salary;
        uint IDt;
        uint payment;
        uint deposit;
        uint count;
    }
    struct Mailman{
        address MailmenAdd;
        bool invoker; 
        uint M;//deposit
        uint index;
        uint salary;
    }

    event Init (uint index);



    uint public i=0;

    function InitPara() external{
        emit Init(i);
    }

    event Published(
        address sender,
        uint IDt);



    mapping(uint=>Sender) public senders;
    mapping(uint=>mapping(uint=>Mailman)) public mailmen;


    function isEqual(bytes memory _a, bytes memory _b) public pure returns (bool) {


        if (_a.length != _b.length) return false;


        for(uint j = 0; j < _a.length; j++) {
            if(_a[j] != _b[j]) {
                // return false;
                return true;
            }
        }
        return true;
    }

    /*
    PubTask
    */

    function PubTask(
        address _Adds,
        string[] memory _SSiHash,
        uint _tfStart,uint _tfEnd,
        uint _payment,uint _n
    )
    payable public returns(uint)
    {
        senders[i]=Sender({
        Adds:_Adds,
        SSiHash:_SSiHash,
        tfStart:_tfStart,
        tfEnd:_tfEnd,
        salary:_payment/_n,
        IDt:i,
        payment:_payment,
        deposit:0,
        count:0
        });



        //if(_Adds==msg.sender){
        //payable(address(this)).transfer(10);
        //}

        uint IDt=i;

        i++;
        emit Published(
            senders[IDt].Adds,
            senders[IDt].IDt);
        return IDt;
    }

    event Registed(uint index);
    /*
        Register
    */

    function Register (uint _IDt,uint _deposit,uint _n) public payable returns (uint){
        //uint _count=senders[_IDt].count;
        if(senders[_IDt].count<_n && mailmen[i][senders[_IDt].count].invoker==false && msg.sender!=senders[_IDt].Adds){
            uint _count=++senders[_IDt].count;

            mailmen[_IDt][_count]=Mailman({
            MailmenAdd: msg.sender,
            invoker: true,
            M: _deposit,
            index: _count,
            salary: 0
            });

            payable(address(this)).transfer(_deposit);

            //deposit[_IDt]=deposit[_IDt]+_deposit;
            senders[_IDt].deposit+=_deposit;
            emit Registed(_count);
            return _count;
        }
        else{
            return 0;
        }
    }

    function Shares (uint _n, string[] memory _Si) public {
        string[] memory share = new string[](_n);
        for(uint j=0; j<_n; j++){
            share[j] = _Si[j];
        }
    }


    function PubShare(uint _IDt,uint _index,string memory _ss,uint _n,uint _pt)  public payable{
        //uint SSiHash=_S.SSiHash[_IDt][_index-1];
        string memory SSiHash=senders[_IDt].SSiHash[_index-1];
        // bytes memory _SSHashbyte;
        // assembly { mstore(add(_SSHashbyte,32),SSiHash) }


        // bytes memory _ssbyte;
        // assembly { mstore(add(_ssbyte,32), _ss) }
        BigNumber.instance memory ss = BigNumber.instance(bytes(_ss), false, 224);

        // BigNumber.instance memory res = g.prepare_modexp(ss,q);
        // bytes memory resval = res.val;
        bytes memory resval = g.prepare_modexp(ss, q).val;


        uint salary=address(this).balance/_n;


        bool Check=isEqual(resval,bytes(SSiHash));
        if( Check==true && _pt>senders[_IDt].tfStart && _pt<senders[_IDt].tfEnd){

            payable(msg.sender).transfer(salary);

            //payment[_IDt]=payment[_IDt]-salary;
            senders[_IDt].payment-=salary;
        }
    }

    function Report(uint _IDt,uint _n, uint _index,string memory _SSe,uint _pt) public payable{

        //uint _SSeHash=_S.SSiHash[_IDt][_index-1];
        string memory _SSeHash=senders[_IDt].SSiHash[_index-1];
        // bytes memory _SSebyte;
        // assembly { mstore(add(_SSebyte,32), _SSe) }

        // bytes memory _SSeHashbyte;
        // assembly { mstore(add(_SSeHashbyte,32), _SSeHash) }
        BigNumber.instance memory SSe = BigNumber.instance(bytes(_SSe), false, 224);
        BigNumber.instance memory res = g.prepare_modexp(SSe,q);

        bytes memory resval = res.val;


        uint salary=address(this).balance/_n;


        bool Check=isEqual(resval,bytes(_SSeHash));
        if( Check==true && _pt>senders[_IDt].tfStart && _pt<senders[_IDt].tfEnd ){

            payable(msg.sender).transfer(salary);

            //payment[_IDt]=payment[_IDt]-salary;
            senders[_IDt].payment-=salary;

        }
    }

    function Refund(uint _IDt,uint _n,uint _pt)public payable{
        if(_pt>senders[_IDt].tfStart){

            //payable(msg.sender).transfer(payment[_IDt]);
            payable(msg.sender).transfer(senders[_IDt].payment);


            for(uint k=0;k<_n;k++){
                // uint index=_Mailman.index[_IDt][k];
                // if(_Mailman.M[_IDt][index] != 0){
                //     payable(msg.sender).transfer(_Mailman.M[_IDt][_Mailman.index[_IDt][k]]);
                // }
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