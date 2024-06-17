var z_achse = 0
    var förderband = 0
    var ausfahrer = 0

    var con_established = false;

    function connect_to_client() {
        var start_time = Date.now();

        var ip = document.getElementById("ipv4").value;

        var creds = {
            "username": document.getElementById("username").value,
            "password": document.getElementById("password").value,
        };

        sendData({
            "connect_to_client": { "start_time": start_time, "ip": ip, "creds": creds }
        }, set_connection_return);
    }

    const intervalID = setInterval(keep_con_alive, 110000);

    function keep_con_alive() {
        if (con_established) {
            sendData({ "ping": "" }, function empty() { });
        }
    }

    function enable_testmode() {
        sendData({ "enable_testmode": "" }, set_testwindow);
    }

    function set_testwindow(data) {
        document.getElementById("testwindow").style.display = "block";
        initializeCanvas(); // Ensure the canvas is initialized when the test window is shown
    }

    function set_connection_return(data) {
        document.getElementById("connection_return_data").innerHTML = data;

        if (document.getElementById("status_con").innerHTML == "200") {
            con_established = true;
        }
    }

    function sendData(data, callback) {
        var xhr = new XMLHttpRequest();
        var url = "{{url_for('dashb.control_afss')}}";

        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                callback(xhr.responseText);
            }
        };

        var jsonData = JSON.stringify(data);
        xhr.send(jsonData);
    }

    var alla_before;

    function send_positions() {
        alla = {
            "x": box.x,
            "y": box.y,
            "z": z_achse,
            "a": ausfahrer,
            "f": förderband,
        }
        if (!compareJson(alla_before, alla)) {
            console.log('alla :>> ', alla);
            sendData({ "update_position": alla }, function empty() { })
        }

        alla_before = alla;
    }

    var canvas;
    var ctx;
    var positionDisplay;
    var box = { x: 50, y: 50, width: 50, height: 50 };
    var isDragging = false;
    var offsetX, offsetY;

    function initializeCanvas() {
        canvas = document.getElementById('canvas');
        ctx = canvas.getContext('2d');
        positionDisplay = document.getElementById('position');

        function resizeCanvas() {
            canvas.width = canvasContainer.clientWidth;
            canvas.height = canvasContainer.clientHeight;
            drawBox();
        }

        function drawBox() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'red';
            ctx.fillRect(box.x, box.y, box.width, box.height);
            updatePositionDisplay();
        }

        canvas.addEventListener('mousedown', function (e) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            if (mouseX > box.x && mouseX < box.x + box.width && mouseY > box.y && mouseY < box.y + box.height) {
                isDragging = true;
                offsetX = mouseX - box.x;
                offsetY = mouseY - box.y;
            }
        });

        canvas.addEventListener('mousemove', function (e) {
            if (isDragging) {
                const rect = canvas.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mouseY = e.clientY - rect.top;
                box.x = mouseX - offsetX;
                box.y = mouseY - offsetY;
                box.x = Math.max(0, Math.min(box.x, canvas.width - box.width));
                box.y = Math.max(0, Math.min(box.y, canvas.height - box.height));
                drawBox();
            }
        });

        canvas.addEventListener('mouseup', function () {
            if (isDragging) {
                isDragging = false;
                updatePositionDisplay();
                onBoxRest();
            }
        });

        function getPosition(x, y) {
            console.log(`X: ${x}, Y: ${y}`);
            // Here you can call other functions or perform actions with the x and y values
        }

        function updatePositionDisplay() {
            positionDisplay.textContent = `Position: (X: ${box.x}, Y: ${box.y})`;
        }

        function onBoxRest() {
            send_positions()
        }


        function moveBox(dx, dy) {
            box.x += dx;
            box.y += dy;
            box.x = Math.max(0, Math.min(box.x, canvas.width - box.width));
            box.y = Math.max(0, Math.min(box.y, canvas.height - box.height));
            drawBox();
            updatePositionDisplay();
            onBoxRest();
        }


        document.getElementById('left').addEventListener('click', () => moveBox(-10, 0));
        document.getElementById('right').addEventListener('click', () => moveBox(10, 0));
        document.getElementById('up').addEventListener('click', () => moveBox(0, -10));
        document.getElementById('down').addEventListener('click', () => moveBox(0, 10));

        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        drawBox();
        updatePositionDisplay();
    }

    const slider1 = document.getElementById('slider1');
    const slider2 = document.getElementById('slider2');
    const value1 = document.getElementById('value1');
    const value2 = document.getElementById('value2');
    const leftBtn1 = document.getElementById('leftBtn1');
    const rightBtn1 = document.getElementById('rightBtn1');
    const leftBtn2 = document.getElementById('leftBtn2');
    const rightBtn2 = document.getElementById('rightBtn2');
    const decreaseFörderband = document.getElementById('decreaseFörderband');
    const increaseFörderband = document.getElementById('increaseFörderband');
    const förderbandValue = document.getElementById('förderbandValue');

    let interval;
    let tempValue1 = Number(slider1.value);
    let tempValue2 = Number(slider2.value);
    let tempFörderband = förderband;

    function updateSliderValue(slider, valueElement, variable) {
        valueElement.textContent = slider.value;
        variable = slider.value;
        send_positions()

    }

    slider1.addEventListener('change', () => {
        z_achse = slider1.value;
        updateSliderValue(slider1, value1, z_achse);
        send_positions()
    });

    slider2.addEventListener('change', () => {
        ausfahrer = slider2.value;
        updateSliderValue(slider2, value2, ausfahrer);
        send_positions()
    });

    function startHold(action) {
        interval = setInterval(action, 50);
    }

    function stopHold(finalizeAction) {
        clearInterval(interval);
        finalizeAction();
    }

    function incrementSlider1() {
        tempValue1 = Math.min(Number(slider1.value) + 1, slider1.max);
        slider1.value = tempValue1;
        value1.textContent = tempValue1;
    }

    function decrementSlider1() {
        tempValue1 = Math.max(Number(slider1.value) - 1, slider1.min);
        slider1.value = tempValue1;
        value1.textContent = tempValue1;
    }

    function incrementSlider2() {
        tempValue2 = Math.min(Number(slider2.value) + 1, slider2.max);
        slider2.value = tempValue2;
        value2.textContent = tempValue2;
    }

    function decrementSlider2() {
        tempValue2 = Math.max(Number(slider2.value) - 1, slider2.min);
        slider2.value = tempValue2;
        value2.textContent = tempValue2;
    }

    function incrementFörderband() {
        tempFörderband++;
        förderbandValue.textContent = tempFörderband;
    }

    function decrementFörderband() {
        tempFörderband--;
        förderbandValue.textContent = tempFörderband;
    }

    leftBtn1.addEventListener('mousedown', () => startHold(decrementSlider1));
    rightBtn1.addEventListener('mousedown', () => startHold(incrementSlider1));
    leftBtn2.addEventListener('mousedown', () => startHold(decrementSlider2));
    rightBtn2.addEventListener('mousedown', () => startHold(incrementSlider2));
    decreaseFörderband.addEventListener('mousedown', () => startHold(decrementFörderband));
    increaseFörderband.addEventListener('mousedown', () => startHold(incrementFörderband));

    document.addEventListener('mouseup', () => {
        stopHold(() => {
            z_achse = tempValue1;
            updateSliderValue(slider1, value1, z_achse);

            ausfahrer = tempValue2;
            updateSliderValue(slider2, value2, ausfahrer);

            förderband = tempFörderband;
            förderbandValue.textContent = förderband;
            send_positions()
        });
    });

    document.addEventListener('mouseleave', () => {
        stopHold(() => {
            z_achse = tempValue1;
            updateSliderValue(slider1, value1, z_achse);

            ausfahrer = tempValue2;
            updateSliderValue(slider2, value2, ausfahrer);

            förderband = tempFörderband;
            förderbandValue.textContent = förderband;
            send_positions()
        });
    });

    function compareJson(obj1, obj2) {
        if (typeof obj1 !== 'object' || typeof obj2 !== 'object') {
            return obj1 === obj2;
        }

        if (obj1 === null || obj2 === null) {
            return obj1 === obj2;
        }

        if (Array.isArray(obj1) !== Array.isArray(obj2)) {
            return false;
        }

        if (Array.isArray(obj1)) {
            if (obj1.length !== obj2.length) {
                return false;
            }
            for (let i = 0; i < obj1.length; i++) {
                if (!compareJson(obj1[i], obj2[i])) {
                    return false;
                }
            }
        } else {
            const keys1 = Object.keys(obj1);
            const keys2 = Object.keys(obj2);

            if (keys1.length !== keys2.length) {
                return false;
            }

            for (let key of keys1) {
                if (!compareJson(obj1[key], obj2[key])) {
                    return false;
                }
            }
        }

        return true;
    }
