var updateBtns = document.getElementsByClassName('update-cart')
let elements = document.getElementsByName('eventlistBtn');
let itemcheckbox = document.getElementsByName('itemcheckbox');
let quantity = document.getElementsByName('quantity');


function activateButton() {
	var listBtnElement = document.activeElement
	for (i = 0; i < elements.length; i++) {
		listBtnElement.classList.add('active')
		if (listBtnElement.id == elements[i].id) {
			listBtnElement.classList.add('active')
		} else {
			elements[i].classList.remove('active')
		}
	}
}

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('focusout', function(e){

		var itemId = this.dataset.item
		var action = this.dataset.action

		console.log('itemIssssd:', itemId, 'Action:', action)
		console.log('USER:', user)

		var quantity = document.getElementById(itemId).value
		console.log('quantity:', quantity)

		if (user =='AnonymousUser'){
			addCookieItem(itemId, action)
		}else{
			updatePledgedItem(itemId, action, quantity)
		}

	})
}

function checkCartField(object) {
	let phone = document.getElementsByName('phone');
	let fullname = document.getElementsByName('fullname');
	let region = document.getElementById ( "region" ).value.trim();
	let center = document.getElementById ( "center" ).value;
	if (phone[0].value == '' || fullname[0].value == '' || region == '' || center == '') {
		document.getElementById("errordiv").innerHTML = "Please populate value for required fields under 'User Info' section"
		document.getElementById("errordiv").classList = "alert alert-danger"
		return false;
	}
	var authcode = ''
	var generatedcode = ''
	try {
		authcode = document.getElementsByName(authcode)[0].value;
		generatedcode = document.getElementsByName (generatedcode)[0].value;
	} catch (error) {
		authcode = document.getElementsByName('authcode')[0].value;
		generatedcode = document.getElementsByName ('generatedcode')[0].value;
		console.error(error);
	}
	if (generatedcode == authcode) {
		return true;
	} else {
		document.getElementById("errordiv").innerHTML = "Error matching 'Auth Code'. Please check your input and try again."
		document.getElementById("errordiv").classList = "alert alert-danger"
	}
	return false;
}

function populateSaiCenter(object) {
	
	var url = 'updateItem/'
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'selectedCenter':center.value.trim(), 'selectedRegion':region.value.trim()})
	})
	.then((response) => {
		return response.json();
	 })
	.then((data) => {
		location.reload()
	});
}

function removeItem(object) {
	var url = 'updateItem/'

	var action = object.dataset.action
	var itemid = object.dataset.itemid
	var eventid = object.dataset.eventid
	var quantity = object.dataset.quantity
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify(
			{'itemid':itemid, 'action':action, 
					'eventid': eventid, 'quantity' : quantity, 
					'selectedCenter':center.value.trim(), 
					'selectedRegion':region.value.trim()
			}
		)
	})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		location.reload()
	});
}

function maxLengthCheck(object) {
	if (parseInt(object.value) > parseInt(object.max) && object.value.length >= object.max.length) {
		document.getElementById("errordiv").innerHTML = "Please enter quantity less than required quantity"
		document.getElementById("errordiv").classList = "alert alert-danger"
	} else {
		document.getElementById("errordiv").classList = "alert alert-danger d-none"
	}
	for (i = 0; i < itemcheckbox.length; i++) {
		if (object.id == itemcheckbox[i].id) {
			if (parseInt(object.value) > 0) {
				itemcheckbox[i].checked = true
				itemcheckbox[i].disabled = false
			} else if (itemcheckbox[i].checked) {
				itemcheckbox[i].checked = false
				itemcheckbox[i].disabled = true
			}
		}
	}
}

function checkemailid(object) {
	let EmailId = document.getElementsByName('EmailId');
	let region = document.getElementsByName('region');
	if (region[0].value.trim().length == 0) {
		document.getElementById("errordiv").innerHTML = "Please select a valid region"
		document.getElementById("errordiv").classList = "alert alert-danger"
		return false
	}
	if (EmailId[0].value == '' )
	{
		document.getElementById("errordiv").innerHTML = "Please enter valid email address to proceeed"
		document.getElementById("errordiv").classList = "alert alert-danger"
		return false
	} else {
		let notfound = true
		for (i = 0; i < quantity.length; i++) {
			if (quantity[i].value > 0) {
				notfound = false
			}
		}
		if (notfound) {
			document.getElementById("errordiv").innerHTML = "Please enter non zero value in quantity field to proceed"
			document.getElementById("errordiv").classList = "alert alert-danger"
			return false
		}
	}
	return true
}

function resetQuantity(object) {
	for (i = 0; i < quantity.length; i++) {
		if (object.id == quantity[i].id) {
			if (!object.checked) {
				quantity[i].value = ''
				object.disabled = true
			}
		}
	}
}