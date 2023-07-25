//  add to cart button ajax
$(".addToCartButton").on('click', function() {
    console.log("add to cart button clicked")

    var productid = document.getElementById("productid").value;
    var selectedcolor = document.getElementById("selectedcolor").value;
    var selectedsize = document.getElementById("selectedsize").value;
    var selectedprice = document.getElementById("selectedprice").value;
    var selectedquantity = document.getElementById("quantity").value;
  
    console.log(productid)

    data = {"productid" : productid,"selectedcolor":selectedcolor,"selectedprice":selectedprice,"selectedquantity":selectedquantity}

    $.ajax({
       url:"{% url 'add_to_cart' %}",
       method:"GET",
       data:data,

       success: function(data) {
          console.log("code run success")
          console.log(data.status)
          console.log(data.message)
       }
   })

})