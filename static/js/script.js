const displayFilter = () => {
	const gridCheck = document.getElementById("gridCheck");
	const datafilter = document.getElementById("datafilter");
	console.log("gridheck---- " + gridCheck);
	console.log("datafilter---- " + datafilter);
	if (gridCheck != undefined && gridCheck != undefined) {
		if (gridCheck.checked) {
			datafilter.classList.remove('d-none');
		} else {
			datafilter.classList.add('d-none');
		}
	}
}
