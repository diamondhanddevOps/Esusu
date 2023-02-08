<script>
  document.addEventListener("DOMContentLoaded", function() {
    // Get form element
    const form = document.querySelector("form");
    
    // Submit event listener
    form.addEventListener("submit", function(event) {
      event.preventDefault();
      
      // Get form data
      const name = document.querySelector("#name").value;
      const email = document.querySelector("#email").value;
      const message = document.querySelector("#message").value;
      
      // Display form data in console
      console.log("Name: " + name);
      console.log("Email: " + email);
      console.log("Message: " + message);
    });
  });
</script>