// document.onload({});

$('#new').on('click', function() {

	$.ajax({
		url:"/create?render=yes&company=kuku", 
		type:'get',
		success: function(response){
			console.log(response);
			window.location = '/create?render=yes';
		}
	});
});

$('#recordForm').submit(function (e) {
	// body...
	e.preventDefault();
	var truck_num = $('#truckNum').val();
	var company = $('#compName').val();
	var bon_num = $('#bonNum').val();
	var expenses = $('#exps').val();
	var income = $('#income').val();
	$.ajax({
		url:"/create?truck_num="+truck_num+"&company='"+company+"'&bon_num="+bon_num+"&expenses="+expenses+"&income="+income, 
		type:'get',
		// data: {truck_num:truck_num,company:company,bon_num:bon_num,expenses:expenses,income:income}
		success: function(response){
			window.location = '/status?title='+response.title+'&msg='+response.msg;
		}
	});
}

);

function goHome(){
	window.location='/';
}