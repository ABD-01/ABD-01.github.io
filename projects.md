---
hide-toc: true
---

# Projects

Explore my projects below.

Want to see more? Head over to my [{fab}`github` GitHub profile](https://github.com/ABD-01) for more comprehensive look.

<style>
    .one {
      /* width: 160px; */
      /* height: 160px; */
      position: relative;
    }

    .two {
      width: 100%;
      height: 100%;
      position: absolute;
      transition: opacity .2s ease-in-out;
      -moz-transition: opacity .2s ease-in-out;
      -webkit-transition: opacity .2s ease-in-out;
    }

    .fade {
      transition: opacity .2s ease-in-out;
      -moz-transition: opacity .2s ease-in-out;
      -webkit-transition: opacity .2s ease-in-out;
    }

    .self-name {
      font-weight: bold;
      text-decoration: underline;
    }

</style>

`````{grid}
:class-container: sd-shadow-lg

````{grid-item}
:columns: 3
:class: sd-align-major-center

```{image} _static/images/cvp-removebg.png

```

````

````{grid-item}
:columns: 9

### [Connected Vehicle Protocol Server](https://abd-01.github.io/Flask-Protobuf/)
[project page](https://abd-01.github.io/Flask-Protobuf/) | [code](https://github.com/ABD-01/Flask-Protobuf)

The CVP Proto Server is a Flask-based application designed for handling MQTT communication with protobuf-encoded telemetry messages for connected vehicles. It features a user-friendly web interface with real-time updates via Socket.IO, and also includes a Command Line Interface (CLI) for direct command-response operations.
````

`````

<!-- 
`````{grid}
:class-container: sd-shadow-lg

````{grid-item}
:columns: 3
:class: one
<div class="two sd-row" id='hello'>
<video  width=100% height=100% muted autoplay loop><source src="/images/ivpreds.mp4" type="video/mp4">Your browser does not support the video tag.</video>
</div>
<img src='/images/triplet_net.png' onmouseout="hello_stop()" onmouseover="hello_start()">
````

````{grid-item}
:columns: 9
### Face Unlock

Muhammed Abdullah, Khurshed Fitter, Rishika Bhagwatkar
project page | pdf | code

This project implemented Triplet Network and FaceNet algorithms from scratch with ResNet as the backbone architecture for face recognition. It was developed at IvLabs for one-shot and few-shot learning on different datasets and with the goal of deploying it as a face recognition-based door lock system.
````

<script type="text/javascript">
    function hello_start() {
        document.getElementById('hello').style.opacity = "1";
    }
    function hello_stop() {
        document.getElementById('hello').style.opacity = "0";
    }
    hello_stop()
</script>

````` 
-->


`````{grid}
:class-container: sd-shadow-lg

````{grid-item}
:columns: 3
:class: sd-align-major-center

```{image} https://abd-01.github.io/images/Arch.png
:alt: Architecture

```

````

````{grid-item}
:columns: 9

### [Open-Set Multi-Source Multi-Target Domain Adaptation](https://ivlabs.github.io/os-nsmt/)
[Rohit Lal](http://rohitlal.net/), [Arihant Gaur](https://gaurarihant.github.io/), [Aadhithya Iyer](https://aadhithya14.github.io/), [Muhammed Abdullah Shaikh]{.self-name}, [Ritik Agrawal](https://www.linkedin.com/in/ritik-agrawal-6b7718189/), [Shital Chiddarwar](https://mec.vnit.ac.in/people/sschiddarwar/)\
*Pre-Registration Workshop, NeurIPS, 2021* \
[project page](https://ivlabs.github.io/os-nsmt/) | [arXiv](https://arxiv.org/abs/2302.00995) | [video](https://youtu.be/dflYL6WBZI4) | [code](https://github.com/IvLabs/os-nsmt)

This work introduced a new setting for unsupervised domain adaptation and utilized a prototypical network to create domain embeddings. We used the Local Outlier Factor (LOF) to pseudo-label unknown classes, and used graph neural networks with attentional aggregation for the adaptation stage.
````

`````

<table style="width:100%;border:0px;border-spacing:0px;border-collapse:separate;margin-right:auto;margin-left:auto;"><tbody>

<!-- Face Unlock -->
<tr onmouseout="face_stop()" onmouseover="face_start()" class="sd-shadow-lg">
<td style="padding:20px;width:25%;vertical-align:middle">
    <div class="one">
    <div class="two" id='face_image'><video  width=100% height=100% muted autoplay loop>
    <source src="/images/ivpreds.mp4" type="video/mp4">
    Your browser does not support the video tag.
    </video></div>
    <img src='/images/triplet_net.png'>
    </div>
<script type="text/javascript">
    function face_start() {
        document.getElementById('face_image').style.opacity = "1";
        var twoElement = document.getElementById('face_image');
        twoElement.style.opacity = "1";
        twoElement.nextElementSibling.style.opacity = "0";
    }
    function face_stop() {
        var twoElement = document.getElementById('face_image');
        twoElement.style.opacity = "0";
        twoElement.nextElementSibling.style.opacity = "1";
    }
    face_stop()
</script>
</td>
<td style="padding:20px;width:75%;vertical-align:middle">
    <a href="https://bit.ly/unlockface">
    <h3>Face Unlock</h3>
    </a>
    <strong style="text-decoration: underline;">Muhammed Abdullah</strong>,
    <a href="https://sites.google.com/view/kpfitter">Khurshed Fitter</a>,
    <a href="https://www.linkedin.com/in/rishika-bhagwatkar-01069518b/">Rishika Bhagwatkar</a>
    <br>
    <a href="https://wandb.ai/abd1/Face-Unlock/reports/Face-Unlock--VmlldzoxMzEyNjQ4">project page</a>
    |
    <a href="https://drive.google.com/file/d/1dUgs0scuxf6f7TJywUj7D6P3bfmro6eJ/view?usp=sharing">pdf</a>
    |
    <a href="https://github.com/IvLabs/Face-Unlock">code</a>
    <p></p>
    <p>
    This project implemented Triplet Network and FaceNet algorithms from scratch with ResNet as the backbone architecture for face recognition. It was developed at IvLabs for one-shot and few-shot learning on different datasets and with the goal of deploying it as a face recognition-based door lock system.
    </p>
</td>
</tr>						

<!-- Object Detection -->
<tr onmouseout="nlt_stop()" onmouseover="nlt_start()" class="sd-shadow-lg">
<td style="padding:20px;width:25%;vertical-align:middle">
    <div class="one">
    <div class="two" id='nlt_image'><video  width=100% height=100% muted autoplay loop>
    <source src="/images/Racoon.m4v" type="video/mp4">
    Your browser does not support the video tag.
    </video></div>
    <img src='/images/racoon2.png'>
    </div>
    <script type="text/javascript">
    function nlt_start() {
        var twoElement = document.getElementById('nlt_image');
        twoElement.style.opacity = "1";
        twoElement.nextElementSibling.style.opacity = "0";
    }
    function nlt_stop() {
        var twoElement = document.getElementById('nlt_image');
        twoElement.style.opacity = "0";
        twoElement.nextElementSibling.style.opacity = "1";
    }
    nlt_stop()
</script>
</td>
<td style="padding:20px;width:75%;vertical-align:middle">
    <a href="https://github.com/IvLabs/Object-Detection">
    <h3>Object Detection</h3>
    </a>
    <a href="https://www.linkedin.com/in/harsh-sharma-018206233/">Harsh Sharma</a>,
    <a href="https://www.linkedin.com/in/rajashree-tekaday-261582205/">Rajashree Tekaday</a>,
    <strong style="text-decoration:underline;"> Muhammed Abdullah</strong>
    <br>
    <a href="https://github.com/IvLabs/Object-Detection">code</a>
    <p></p>
    <p>This project is an implementation of a sliding window technique with a two-stage detector, enhanced with the Overfeat framework, for object detection on a Raccoon Dataset.</p>
</td>
</tr> 
        
<!-- ROS PID -->
<tr onmouseout="tb_stop()" onmouseover="tb_start()" class="sd-shadow-lg">
<td style="padding:20px;width:25%;vertical-align:middle">
    <div class="one">
    <div class="two" id='tb_image'><video  width=100% height=100% muted autoplay loop>
    <source src="/images/turtlebot.m4v" type="video/mp4">
    Your browser does not support the video tag.
    </video></div>
    <img src='/images/turtlebot.jpg'>
    </div>
    <script type="text/javascript">
    function tb_start() {
        var twoElement = document.getElementById('tb_image');
        twoElement.style.opacity = "1";
        twoElement.nextElementSibling.style.opacity = "0";
    }
    function tb_stop() {
        var twoElement = document.getElementById('tb_image');
        twoElement.style.opacity = "0";
        twoElement.nextElementSibling.style.opacity = "1";
    }
    tb_stop()
</script>
</td>
<td style="padding:20px;width:75%;vertical-align:middle">
    <a href="https://github.com/ABD-01/ros_pid">
    <h3>PID Control and Path Planning for TurtleBot in ROS</h3>
    </a>
    <strong style="text-decoration: underline;">Muhammed Abdullah</strong>
    <br>
    <a href="https://github.com/ABD-01/ros_pid">code</a>
    <p></p>
    <p>This project involved implementing a PID controller on a TurtleBot robot to perform a Goal-to-Goal task and Path Planning task. The controller was modeled using a Hermite curve to generate a trajectory for the robot's motion from the initial to the goal pose.</p>
</td>
</tr>

</tbody></table>


## Mini-Projects

`````{grid}
:class-container: sd-shadow-lg

````{grid-item}
:columns: 3
:class: sd-align-major-center

```{image} _static/images/under-construction.png
:alt: under-construction.png
:align: center
:width: 50%
```

````

````{grid-item}
:columns: 9

\# TODO

````
`````


`````{grid}
:class-container: sd-shadow-lg

````{grid-item}
:columns: 3
:class: sd-align-major-center

```{image} https://github.com/Muhammed-Abdullah-Shaikh/bezier/blob/master/media/bezier_demo.gif?raw=true

```

````

````{grid-item}
:columns: 9

### Bezier Curves

\# TODO

````

`````


## I would like you opinion on this project page:

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
      "content": "<@701479951479865384>, you have a new message from the website (project page)!",
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
