var modal = document.getElementById("create_modal");
var btn = document.getElementById("create_button");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

document.addEventListener('keydown', function(e)
{if(e.key === 'Escape')
	modal.style.display = "none";
	})