# Miscellaneous

```{image} _static/images/under-construction.png
:alt: under-construction.png
:align: center
:width: 40%
```

## You can suggest me of any ideas here:

````{grid} 1 1 1 2
```{raw} html

<style>
   #ContactForm{
      form {
         padding: 25px;
         margin: 25px;
      }

      input,
      textarea {
         width: 90%;
         padding: 8px;
         margin-bottom: 20px;
         border: 1px solid var(--color-brand-primary);
         outline: none;
         color: var(--color-content-foreground);
         background-color: var(--color-admonition-title-background--admonition-todo);
      }

      button {
         width: 30%;
         padding: 10px;
         border: none;
         background: var(--color-admonition-title-background--seealso);
         font-size: 16px;
         font-weight: 400;
         color: var(--color-admonition-title--seealso);
         ;
      }

      button:hover {
         background: #2371a0;
      }

      @media (min-width: 568px) {
         .main-block {
               flex-direction: row;
         }
      }
   }
</style>
<form id="ContactForm" onsubmit="event.preventDefault();">
    <div class="info">
        <input class="fname" type="text" name="name" placeholder="Name">
        <input type="text" name="email" placeholder="Email">
    </div>
    <p>Message</p>
    <div>
        <textarea name="message" rows="4" style="width: 90%;"></textarea>
    </div>
    <button id="submitButton">Submit</button>
</form>

<script>
var submitMessage = document.getElementById("submitButton"),
    ContactForm = document.getElementById("ContactForm");

function submit(){
  const whToken = lfcbu47('UzJabm1KSlBoNjl4TXQ4eE5ZbkNpdi1MVlBwZHdSWnpFYWVrc1J5Zmg2ZzRUUEpRYnZvXzR0NWxRYWthMk1IWHdYMl8=');
  const whId = lfcbu47('MTQxNzgyMTMxNTgwODc1OTgzOA==');
  const d = lfcbu47("ZGlzY29yZC5jb20vYXBpL3dlYmhvb2tz");
  var url = `https://${d}/${whId}/${whToken}`;

  var xhr = new XMLHttpRequest();
  xhr.open("POST", url);

  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      console.log(xhr.status);
      console.log(xhr.responseText);
      alert(xhr.status === 200 || xhr.status === 204 ? 'Message Sent' : 'Failed to send message');
    }};

  var data = {
  "content": "<@701479951479865384>, you have a new message from the website!",
  "embeds": [
    {
      "title": ContactForm.name.value,
      "description": "**Email**:" + ContactForm.email.value + "\n**Message**:" + ContactForm.message.value,
      "color": 22963
    }
  ]
  };
  xhr.send(JSON.stringify(data));
}

submitMessage.addEventListener('click',()=>{
    submit();
    alert("Message Sent")
})
</script>

```
````
