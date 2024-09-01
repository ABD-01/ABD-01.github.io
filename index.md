---
hide-toc: true
---


# Welcome to My Corner of the Web

```{toctree}
---
maxdepth: 2
caption: Contents
hidden:
---

Home <self>
About <about>
Archive <archive>
Projects <projects>
Notes <notes>
Misc <misc>
Resume <resume>
```

Hey there! <img src="/assets/img/Hi.gif" style="height: 1.5em;"> 

I'm thrilled you dropped by. This is my personal space where I keep a lot of things such as notes, interesting tidbits, and random discoveries I gather along the way. Think of it as a friendly journal where I jot down things I find interesting and helpful or maybe because I do not want to forget them.

Whether you're a fellow enthusiast or just curious, I hope you find something valuable here. 

If you like to use RSS, you can follow me via the RSS link [here](posts/atom.xml){.external}.


## News

<ul>
   <li data-marker="*">
      <strong>June 2023</strong>: Joined <a href="https://accoladeelectronics.com/">Accolade Electronics Pvt. Ltd</a> as an Embedded Software Engineer, working on automotive electronics. and Software Defined Vehicles (SDVs).
   </li>
   <li data-marker="*">
      <strong>May 2023</strong>: Graduated with a B.Tech in Electrical and Electronics Engineering from <a href="https://vnit.ac.in/">Visvesvaraya National Institute of Technology (VNIT)</a> 
   </li>
   <li data-marker="*">
      <strong>June 2022</strong>: Joined <a href="https://www.iitg.ac.in/dsai/">IIT Guwahati</a> under <a href="https://krmopuri.github.io/">Prof. Konda Reddy</a> as a Research Intern.
   </li>
   <li data-marker="*">
      <strong>Oct 2021</strong>: Our paper <a href="https://ivlabs.github.io/os-nsmt/">Open-Set Multi-Source Multi-Target Domain Adaptation</a> got accepted at <a href="https://preregister.science/">Pre-registration Workshop, NeurIPS'21</a>.
   </li>
   <li data-marker="*">
      <strong>September 2021</strong>: <a href="https://github.com/pytorch/vision/pull/4255">Contributed</a> a dataset class for <a href="https://paperswithcode.com/dataset/lfw">Labeled Faces in the Wild (LFW)</a> to <a href="https://github.com/pytorch/vision">Torchvision</a>, a popular computer vision library.
   </li>
   <li data-marker="*">
      <strong>May 2020</strong>: Joined <a href="https://ivlabs.in/">IvLabs, the AI and Robotics Lab</a> led by <a href="https://mec.vnit.ac.in/people/sschiddarwar/">Prof. Shital Chiddarwar</a> as an undergraduate student researcher, working on computer vision, IoT and robotics.
   </li>
</ul>


## Latest Posts

```{eval-rst}
.. postlist:: 3
   :date: %A, %B %d, %Y
   :format: {title}
   :excerpts:
   :expand: Read more ...
```

## Get in Touch:

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
    var url = "https://discord.com/api/webhooks/1205925744660971580/y5by-FiA8G058BiGApiSjZb1enCXGMnkTmIq_dAaGXxg6LXFAz6FV2qNbtcWahk4DApA";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);

    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
       if (xhr.readyState === 4) {
          console.log(xhr.status);
          console.log(xhr.responseText);
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