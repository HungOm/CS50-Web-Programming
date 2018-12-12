document.addEventListener('DOMContentLoaded', () => {
 
	//Connect to socketio

	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	// when connected, instruct what to do
    socket.on('connect', () => {

    	document.querySelectorAll('button').forEach(button => {
    		button.onclick = () => {
    			const selection = button.dataset.vote;
    			socket.emit('submit vote', {'selection':selection});
    		};
    	});

    });

// when the vote is announced, add to the ordered list 

	socket.on('announce vote', data =>{

		const li = document.createElement('li');
		li.innerHTML = `Vote recorded: ${data.selection}`;
		document.querySelector('#votes').append(li);
	});
});