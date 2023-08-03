function convertStringToArray(arrayString) {
    const trimmedString = arrayString.slice(1, -1);
    const elements = trimmedString.split(", ");
    const resultArray = elements.map(element => element.trim().slice(1, -1));
    return resultArray;
}
let booked = [];
let total_price=0.0
let reserved_seats=[]
jQuery.noConflict();
let flag=true
jQuery(document).ready(function($) {
    let re_seats=convertStringToArray($("#booked_seats_id").val())
    if(re_seats[0]!=''){
        re_seats.forEach(seat => {
            console.log("THis is reason")
            $("[id="+seat+"]:eq(1)").css("background","red")
            $("[id="+seat+"]:eq(1)").css("cursor","not-allowed")
            reserved_seats.push(seat)
        }); `   `
    }
    console.log(reserved_seats)
    $("input").click(function(e) {
        let limit=parseInt($("#limit").val())
        let id = $(this).attr('id');
        let val=$(this).attr('value');
        if(booked.length>=limit){
            flag=false 
            if(!booked.includes(id)){
                $("[id="+id+"]:eq(1)").css("background-color","#5bfc60");
            }
        }
        else flag=true
        if(reserved_seats.includes(id)){
            $("[id="+id+"]:eq(1)").css("background-color","red");
        }
        let b_price=parseFloat($("#price_business").val())
        let e_price=parseFloat($("#price_economy").val())
        if (booked.includes(id) && !reserved_seats.includes(id)) {
            if((val[0]=='1' || val[0]=='2' || val[0]=='3') && val[1]!='0'){
                total_price-=b_price
                $("[id="+id+"]:eq(1)").css("background-color","#5bfc60");
            }else{
                total_price-=e_price
                $("[id="+id+"]:eq(1)").css("background-color","#5bfc60");
            }
            booked.splice(booked.indexOf(id), 1);
        } else if(flag && !reserved_seats.includes(id)) {
            if((val[0]=='1' || val[0]=='2' || val[0]=='3')  && val[1]!='0'){
                total_price+=b_price
            }else total_price+=e_price
            $("[id="+id+"]:eq(1)").css("background-color","#656e65");
            booked.push(id);
        }
        console.log(booked)
        $("#count").text(booked.length);
        $("#price").text(total_price)
        $("#selected_seats").val(booked)
        console.log($("#selected_seats").val())
    });

});

