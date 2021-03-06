// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").live("submit", function() {
        newMessage($(this));
        return false;
    });
    $("#messageform").live("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#setNameId").live("submit", function() {
        changeName();
        return false;   //to stop before it goes to a/message/new
    });
    $("#setNameId").live("keypress", function(e) {
        if (e.keyCode == 13) {
            changeName();
            return false;       //to stop before it goes to a/message/new
        }
    });
   
    $("#message").select();
    updater.start();
});

function changeName() {
        var newname = document.setName.username.value;
        if (newname.length < 1) {
            alert("Invalid name");
            return false;
        } else if (newname.length > 12) {
            alert("Error 27: Invalid name:");
            return false;
        }

        updater.name = newname;
        //alert("Your new Name: " + updater.name);
        return false;
        // fejl hvis disse kaldes før return false; ???? why?
        //$("#usernameText").value("");           // slet navnet ?? 
        //$("#message").select();
        //document.getElementById("usernameText").value("");     // slet navnet ??  
        return false;
        //this.find("input[type=text]").val("").select();
}

function newMessage(form) {
    var message = form.formToDict();
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

function target(player) {
    var info = player+"";       // "convert" to string by adding + "";
    message={}
    message["method"]="target";
    message["body"]=player;
    message["name"]=updater.name;
    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {}
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    json["method"] = "chat";
    json["name"] = updater.name;
    if (json.next) delete json.next;
    return json;
};

var updater = {
    name: "random name",
    socket: null,

    start: function() {
        var url = "ws://" + location.host + "/chatsocket";
	updater.socket = new WebSocket(url);
	updater.socket.onmessage = function(event) {
	    updater.showMessage(JSON.parse(event.data));
	}
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};