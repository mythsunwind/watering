function decrease_seconds(pump) {
	element = document.querySelector('#pump' + pump + '_seconds');
	if (Number(element.value) > 0.5) {
		element.value = Number(element.value) - 0.5;
		element.onchange();
	}
}

function increase_seconds(pump) {
	element = document.querySelector('#pump' + pump + '_seconds');
	element.value = Number(element.value) + 0.5;
	element.onchange();
}

function decrease_hour(pump) {
	var element = document.querySelector('#pump' + pump + '_hour');
	if (Number(element.value) > 0) {
		element.value = Number(element.value) - 1;
		element.onchange();
	}
}

function increase_hour(pump) {
	var element = document.querySelector('#pump' + pump + '_hour');
	if (Number(element.value) < 24) {
		element.value = Number(element.value) + 1;
		element.onchange();
	}
}

function toggle_day(pump, day) {
	element = document.querySelector('#pump' + pump + '_day' + day);
	element.classList.toggle("active");
}

function update_pump(number) {
	pump = {}
	pump.id = number
	pump.name = number
	pump.hour = document.querySelector('#pump' + number + '_hour').value
	pump.milliseconds = Number(document.querySelector('#pump' + number + '_seconds').value) * 1000
	pump.days = "123456"
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/pump/' + number, true);
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onload = function () {
		// Request finished. Do processing here.
	};

	xhr.send(JSON.stringify(pump));
}

function test_pump(number) {
	test = {}
	result = window.prompt("Run pump " + number + " for following seconds:", Number(document.querySelector('#pump' + number + '_seconds').value));
	if (result != null) {
		test.milliseconds = Number(result) * 1000
	}
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/pump/' + number + "/test", true);
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onload = function () {
		// Request finished. Do processing here.
	};

	xhr.send(JSON.stringify(test));
}
