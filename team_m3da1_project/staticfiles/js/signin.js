const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}

const passwordField = document.querySelector("#password");
const eyeIcon= document.querySelector("#eye");

eye.addEventListener("click", function(){
	this.classList.toggle("fa-eye-slash");
	const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
	passwordField.setAttribute("type", type);
})


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});