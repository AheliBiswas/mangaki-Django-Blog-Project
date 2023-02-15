console.log("Let's load");

const spinner = document.getElementById('pre-loader');
$.ajax({
  type: 'GET',
  url:'',
  success: function(response){
      setTimeout(()=>{
      spinner.classList.add('not-visible')
      console.log('loading success')
    }, 500)
  },
  error: function(error){
    console.log(error)
  }
})
  

function sendMail(){
  var params ={
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    message: document.getElementById("message").value,
  };
  const serviceID ="service_5mfqfz1";
  const templateID ="template_5zcuesi"

  emailjs.send(serviceID,templateID,params)
  .then(
    (res)=>{
      document.getElementById("name").value ="";
      document.getElementById("email").value ="";
      document.getElementById("message").value ="";
      console.log(res);
      alert("Your message send successfully");
    }
  )
  .catch((err) => console.log(err))
};

