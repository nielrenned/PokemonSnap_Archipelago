var server = new Server();
var port = 48080;
var ip = "127.0.0.1";

var install_directory = pj64.installDirectory;
var config_path = install_directory + "Config\\Project64.cfg";
console.log("PJ64 Config path: " + config_path);

try {
    var file = fs.readfile(config_path.toString()).toString();
    var lines = file.split("\n");
    for (var i = 0; i < lines.length; i++) {
        var cleanLine = lines[i].trim().toLowerCase();
        if (cleanLine.indexOf("psnap_ap_port=") === 0) {
            var portVal = lines[i].split("=")[1].trim();
            var parsedPort = parseInt(portVal, 10);
            if (!isNaN(parsedPort)) {
                port = parsedPort;
                console.log("Port number in Project64.cfg: " + port);
            }
            break;
        }
    }
} catch (e) {
    console.log("Error reading config, using fallback port: " + port);
}

var MemoryBridge = {
    read: function(type, address, size) {
        var result = [];
        if (type === "bytestring") {
            for (var i = 0; i < size; i++) {
                result.push(String.fromCharCode(mem.u8[address + i]));
            }
            return result.join("");
        }

        var step = (type === "u32") ? 4 : (type === "u16") ? 2 : 1;
        var view = mem[type];

        for (var i = 0; i < size; i += step) {
            result.push(view[address + i]);
        }
        return result;
    },

    write: function(type, address, value) {
        if (type === "bytestring") {
            for (var i = 0; i < value.length; i++) {
                mem.u8[address + i] = value.charCodeAt(i);
            }
            return true;
        }

        var step = (type === "u32") ? 4 : (type === "u16") ? 2 : 1;
        var view = mem[type];

        for (var i = 0; i < value.length; i++) {
            view[address + (i * step)] = value[i];
        }
        return true;
    }
};

function startServer() {
    console.log("Starting server...");
    server.listen(port, ip);

    server.on('connection', function(client) {
        console.log("Client connected");
        var isConnected = true;

        client.on('data', function(data) {
            if (!isConnected) return;

            var message = data.toString().trim();
            var parts = message.split(':');
            if (parts.length < 2) {
                client.write("ERR:Invalid message format\n");
                return;
            }

            var messageId = parts[0];
            var payload = parts.slice(1).join(':').trim();
            var args = payload.split(" ");
            var command = args[0].toLowerCase();

            switch (command) {
                case "rominfo":
                    client.write(messageId + ":" + JSON.stringify(pj64.romInfo) + "\n");
                    break;

                case "read":
                    var type = args[1];
                    var address = parseInt(args[2], 16);
                    var size = parseInt(args[3], 10);

                    if (isNaN(address) || isNaN(size) || size <= 0) {
                        client.write(messageId + ":Invalid read parameters\n");
                        break;
                    }

                    var dataOut = MemoryBridge.read(type, address, size);
                    var response = (type === "bytestring") ? dataOut : JSON.stringify(dataOut);
                    client.write(messageId + ":" + response + "\n");
                    break;

                case "dict":
                    var rawJson = payload.substring(5).trim();
                    try {
                        var dict = JSON.parse(rawJson);
                        var result = {};
                        for (var key in dict) {
                            var item = dict[key];
                            if (typeof item !== "object") item = { "adr": item };
                            var type = item.type || "u8";
                            var size = item.size || 1;
                            result[key] = MemoryBridge.read(type, item.adr, size);
                        }
                        client.write(messageId + ":" + JSON.stringify(result) + "\n");
                    } catch (e) {
                        client.write(messageId + ":Invalid Dict JSON Format\n");
                    }
                    break;

                case "write":
                    var type = args[1];
                    var address = parseInt(args[2], 16);
                    var rawValue = args.slice(3).join(" ");

                    if (isNaN(address)) {
                        client.write(messageId + ":Invalid Target Address\n");
                        return;
                    }

                    var parsedValue;
                    if (type === "bytestring") {
                        parsedValue = rawValue;
                    } else {
                        try {
                            parsedValue = JSON.parse(rawValue);
                            if (!Array.isArray(parsedValue)) throw new Error();
                        } catch (e) {
                            client.write(messageId + ":Value must be a valid JSON Array\n");
                            return;
                        }
                    }

                    MemoryBridge.write(type, address, parsedValue);
                    client.write(messageId + ":Write successful\n");
                    break;

                default:
                    client.write(messageId + ":Unknown command\n");
                    break;
            }
        });

        function disconnect() {
            if (isConnected) {
                console.log("Client disconnected");
                isConnected = false;
            }
        }

        client.on('end', function() {
            console.log("Client has ended connection")
            disconnect();
        });

        client.on('close', function() {
            console.log("Client has closed connection")
            disconnect();
        });

        client.on('error', function(err) {
            console.log("Connection error: " + err.message);
            disconnect();
            try { client.close(); } catch(e){}
            restartServer();
        });
    });

    server.on('listening', function() {
        console.log("Server is listening on " + ip + ":" + port);
    });

    server.on('error', function(err) {
        console.log("PJ64 AP server error encountered: " + err.message);
        if (err.message.indexOf("(10013)") !== -1) {
            console.log("Port " + port + " already in use.");
            alert("Port " + port + " is currently in use by another program.");
        }
    });
}

function restartServer() {
    console.log("Restarting PJ64 AP server...");
    try { server.close(); } catch(e){}
    server = new Server();
    setTimeout(startServer, 5000);
}

startServer();