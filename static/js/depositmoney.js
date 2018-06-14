				var acc_number;
				function do_initials(){
					
					var url = "accountdetail";
					$.get(url, function(data, status){
							//	console.log(data);
							json = JSON.parse(data);
							//console.log("Data: " + json + "\nStatus: " + status);
							acc_number = json.acc_number;
							document.getElementById("acc_number_label").innerHTML=acc_number;
							document.getElementById("acc_number").value=acc_number;
							 var balance = json.acc_balance;
							 available_balance = balance;
							 document.getElementById("acc_balance").innerHTML=balance;
							
						});
				}
				
				function deposit_money(){
					$("span[id='message']").html('');
					var username = document.getElementById('username').value;
					var amount = $("input[name='amount']").val();
					//alert(username+","+amount+","+acc_number);
					console.log(amount);
					if(amount===''){
						$("span[id='message']").html("<font color=red>Enter amount</font>");
						document.getElementById('amount').focus();
					}else{
						$.post("money.deposit",
						{
							acc_number: acc_number,
							amount:amount
						},
						function(data,status){
							//console.log("Data: " + data + "\nStatus: " + status);
							$("span[id='message']").html(data);
							$("input[name='amount']").val('');
						});
						
						var url = "accountbalance?acc_number="+acc_number;
						$.get(url, function(data, status){
							console.log(data);
							json = JSON.parse(data);
							console.log("Data: " + json + "\nStatus: " + status);
							 var balance = json.balance;
							 document.getElementById("acc_balance").innerHTML=balance;
							 
							
						});
						
					}				
					
				}