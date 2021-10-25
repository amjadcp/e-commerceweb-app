var count = [];
var totel = [];
var subTotel = 0;
$('#paypal-button-container').hide()
$('#btn').hide()

document.getElementById('cod').addEventListener('click', ()=>{
    $('#paypal-button-container').hide()
    $('#btn').show()
})

document.getElementById('online').addEventListener('click', ()=>{
    $('#btn').hide()
    $('#paypal-button-container').show()
})


const updater =(id, btn)=>{
    let data = {
        'csrfmiddlewaretoken' : $('#'+id+'csrf').val() , //'{{ csrf_token }}',
        'id' : id,
    }
    $.ajax({
        url : 'updater',
        method : 'post',
        data : data,
        dataType : 'json',
        success : (responce)=>{
            id = responce.id
            if(typeof count[id]== 'undefined' && btn=='+'){
                count[id]= 1
            }
            else if(typeof count[id]!= 'undefined' && btn=='+'){
                count[id]=count[id] + 1
            }
            else if(typeof count[id]== 'undefined' && btn=='-'){
                count[id]=0
            }
            else{
                if(count[id]==0){
                    count[id] = 0
                }
                else{
                    count[id] = count[id] - 1 
                }
            }
            $('#'+id+'count').html(count[id])
            var qty = responce.qty
            if(qty<count[id]){
                 $('#'+id+'totel').html("OUT OF STOCK")
                $('#subtotel').hide()
            }
            else{
                $('#subtotel').show()
                subTotel = 0;
                $('#'+id+'totel').html('Totel: RS '+count[id]*responce.price)
                totel[id] = count[id]*responce.price
                for(id=0; id<totel.length; id++){
                    if(typeof totel[id] == 'undefined'){
                        totel[id] = 0
                    }
                    subTotel = subTotel+totel[id]
                }
                $('#subtotel').html('SUBTOTEL : '+ subTotel)
            }

        }
    })

}

var check =()=>{
    let index = [];
    for(let i=0; i<count.length; i++){
        if(typeof count[i]== 'undefined'){

        }
        else{
            index.push(i)
        }
    }
    console.log(index)
    let data = {
        'csrfmiddlewaretoken' : $('#csrf').val(), 
        'id' : JSON.stringify({'id':index}), 
         'qty' : JSON.stringify({'qty':count}),
        'subTotel' : subTotel,
        'name' : $('#name').val(),
        'number' : $('#number').val(),
        'email' : $('#email').val(),
        'address' : $('#address').val(),
        'address2' : $('#address2').val(),
        'city' : $('#city').val(),
        'state' : $('#state').val(),
        'pin' : $('#pin').val(),
    }
     console.log(data)
    $.ajax({
        url : 'place_order',
        method : 'post',
        dataType : 'json',
        data : data,
        success : (responce)=>{
            $('#msg').html(responce.message)
        }
    })
}

//paypal
paypal.Buttons({
    // Set up the transaction
    createOrder: function(data, actions) {
        check();
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: subTotel
                }
            }]
        });
    },
    
    // Finalize the transaction
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(orderData) {
            // Successful capture! For demo purposes:
            console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
            var transaction = orderData.purchase_units[0].payments.captures[0];
            alert('Transaction '+ transaction.status + ': ' + transaction.id + '\n\nSee console for all available details');
    
        });
    }

    }).render('#paypal-button-container');  

