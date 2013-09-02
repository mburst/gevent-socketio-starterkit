(function(){
    exports.onConnect = function(client, done){
        done();
    }
    
    exports.sendMessage = function(client, done){
        var x = Math.floor(Math.random()*1000);
        var y = Math.floor(Math.random()*1000);
        client.emit('moved', {"x": x, "y": y});
        done();
    }
})();