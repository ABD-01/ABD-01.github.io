# RoboticsAcademy Challenge

This is my solution to the [RoboticsAcademy Challenge](https://abd-01.github.io/crispy-adventure/_static/GSoC-2024%20RoboticsAcademy%20test.pdf)

## Visual Follow Line

```{raw} html
<div width="100%" align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?si=Po1TyWtwFuKh3fIw&amp;list=PLm14V2PsCoHSIUe9fpO7Uw2PiDVisftWS" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
```

This exercise requires a PID controller to drive an F1 car in race circuit. This has 2 parts:
1. [Computer Vision](#computer-vision)
2. [Control System](#control-system)

### Approach

#### Computer Vision

This part focuses on using OpenCv library to detect the red line in the circuit so that the controller can take actions nased on it.

I have used filtering in HSV space based on the if pixel value is between the given threshold. I have used two HSV thresholds for red colour to create a mask in the region of interest

These are outputs using indivdual thresholds

```{raw} html
<div width="100%" align="center">
<img src="https://abd-01.github.io/crispy-adventure/_static/ra_media/Path_redbound1.jpg" width=40%/>&emsp;
<img src="https://abd-01.github.io/crispy-adventure/_static/ra_media/Path_redbound2.jpg" width=40%/>
</div>
```

Now, using both the masks together we get a better result

```{code-block} python
---
lineno-start: 51
emphasize-lines: 3
---

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask1 | mask2
```

```{image} https://abd-01.github.io/crispy-adventure/_static/ra_media/Path_redbound_both.jpg
---
alt: Path using both Red Thresholds
align: center
width: 70%
---
```

Next, I have used multiple ROIs instead of one, because of the curved nature of the path. For each ROIs I have found the moment and it's distance from the center. The deviation from centre is then calculated by taking the average of these distances.

However, not all distances are weighted equally. The ROI in the centre has the maximum weightage, then it neighbours above and below, and so on. This way the ROI very close to the wheel and farthest from the wheel have less weightage.

To achive this I have used the following function 

(create-symmetric-array)=
```python
def create_symmetric_array(length):
    middle = length // 2
    half = np.arange(1, middle + 1, dtype=float)  # Create an array [1, 2, ..., middle] with float dtype
    arr = np.concatenate((half, [] if length % 2 == 0 else [middle + 1], half[::-1]))  # Concatenate arrays to form the symmetric array
    arr /= np.linalg.norm(arr, ord=1)  # Normalize the array so that the sum of its elements is 1
    return arr
```

The result looks this this:


```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/Rois.png
:align: center
:figwidth: 70%
:alt: Multiple ROIs
:figclass: sidefigure

Enclosed in Green border shows different ROIs, where the white circle is their moments. Cyan colored Line shows the distance from the center and the Blue arrows represent the weightage of these distances. 
```

#### Control System

PID controller has been used to make the car follow the line. The distance from the centre is takes as an error and used in feedback loop for the angular and linear velocity. The angular velocity uses PID while the linear velocity just uses differential controller. The reason being that the car will run a a fixed speed and slow down near turns.

##### Ziegler–Nichols

I have used the [Ziegler–Nichols method](https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method) for tuning this PID controller.

> The "P" (proportional) gain, $K_{p}$ is then increased (from zero) until it reaches the ultimate gain $K_{u}$, at which the output of the control loop has stable and consistent oscillations.
>
> --*Wikipedia (Ziegler–Nichols method)*

So I increased my $K_{p}$ value from $0.001$ to $0.02$. The best performance I saw was at $K_{p} = 0.005$ and we will see that Ziegler–Nichols method will also give the same conclusion.

At $K_{p} = 0.02$ we have unstable oscillations that break the system. Notice the car complete deviates from the centre at the end of the movie.

```{raw} html
<p class="centered">
  <video width="60%" autoplay muted controls>
    <source src="https://abd-01.github.io/crispy-adventure/_static/ra_media/UnSustained_Oscillation.mp4" type="video/mp4" />
    Your browser does not support the video tag.
  </video>
</p>
```

Here are the stable and consistent oscillations giving the value $K_{u} = 0.015$

```{raw} html
<p class="centered">
  <video width="60%" autoplay muted loop controls>
    <source src="https://abd-01.github.io/crispy-adventure/_static/ra_media/Sustained_Oscillation.mp4" type="video/mp4" />
    Your browser does not support the video tag.
  </video>
</p>
```

```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/oscillation_0.015.png
:align: center
:figwidth: 60%
:alt: Sustained Oscillations
:figclass: sidefigure

Error plot for $K_{p} = 0.015$ showing stable and consistent oscillations.
```

Now, with time period $T_{u} = 6 \times 20$, the values of $K_p$, $K_i$ and $K_d$ are found to be

|  Control Type  |     $K_{p}$     |      $K_{i}$      |    $K_{d}$    |
|:--------------:|:---------------:|:-----------------:|:-------------:|
| some overshoot | $0.0049\bar{9}$ | $0.000083\bar{3}$ | $0.19\bar{9}$ |

I have not used these crude values directly, but tune a bit more from this point where $K_{d}$ was changed to $0.002$

##### PID Test

After finalizing the propotional, integral and differential constants, the out put of system on disturbance was tested and gave satisfactory results.


```{raw} html
<p class="centered">
  <video width="60%" autoplay muted loop controls>
    <source src="https://abd-01.github.io/crispy-adventure/_static/ra_media/Pid_Test.mp4" type="video/mp4" />
    Your browser does not support the video tag.
  </video>
</p>

<div width="100%" align="center">
<img src="https://abd-01.github.io/crispy-adventure/_static/ra_media/PID.png" width=40%/>&emsp;
<img src="https://abd-01.github.io/crispy-adventure/_static/ra_media/PID2.png" width=40%/>
</div>
```

### Simulation

For entire simuation watch the YouTube videos.

```{raw} html
<div width="100%" align="center">
<iframe width="49%" src="https://www.youtube.com/embed/ayDQqRfB7KQ?si=4MOnGT5G0ZsAKRTh" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<iframe width="49%" src="https://www.youtube.com/embed/uzrILcWKJwI?si=rs_J8S_AlONXyci4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
```

Here are few clips showing the performance of the PID path following F1 car.

#### Simple World

##### 1. 90° Corner turn

```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/SimpleWorld_90-degree-turn.webp
:align: center
:figwidth: 70%
:alt: Simple World 90-degree Turn
:figclass: sidefigure

90° Corner turn of Simple World
```

##### 2. Hairpin Turn
```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/SimpleWorld_hairpin-turn.webp
:align: center
:figwidth: 70%
:alt: Simple World Hairpin Turn
:figclass: sidefigure

Hairpin turn of Simple World
```

#### Montmeló World

##### 1. La Caixa (sharp 135° left)
```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/MontmeloWorld_LaCaixa-turn.webp
:align: center
:figwidth: 70%
:alt: Montmelo World La Caixa Turn
:figclass: sidefigure

La Caixa, sharp 135° left turn of Montmelo World
```

##### 2. [Crash] Europcar (sharp 75° right)
```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/MontmeloWorld_Europcar-Corner.webp
:align: center
:figwidth: 70%
:alt: Montmelo World Europcar Corner
:figclass: sidefigure

Europcar corner, sharp 75° right turn of Montmelo World
```

##### 3. [Crash] Chicane 
```{figure} https://abd-01.github.io/crispy-adventure/_static/ra_media/MontmeloWorld_chicane.webp
:align: center
:figwidth: 70%
:alt: Montmelo World Chicane
:figclass: sidefigure

Left-Right Chicane of Montmelo World
```

### Source Code

````{dropdown} PID_controller.py

The source code is available on [github](https://github.com/ABD-01/crispy-adventure/tree/master/RoboticsAcademy) but has been encrypted.
To view the code follow these commands
```bash
wget https://raw.githubusercontent.com/ABD-01/crispy-adventure/master/RoboticsAcademy/PID_controller.py.data
openssl enc -aes-128-cbc -d -a -pbkdf2 -in PID_controller.py.data -out PID_controller.py
```
The key to decrypt the file has been provided in the email. 
````

## Symmetric Arrays

````{dropdown} Symmetric Arrays
:open:

Although that is not what I intended. I wanted to weight the distances such that the weights form a normal distribution.
Something like this:
```python
num = 50
weights = norm.pdf(np.arange(num), num // 2, num//4)
plt.bar(np.arange(num) , weights)
```
```{image} https://abd-01.github.io/crispy-adventure/_static/ra_media/symmetric_array_pdf.png
---
alt: Symmetric Normally Distributed Array
align: center
width: 60%
class: only-light
---
```
```{image} https://abd-01.github.io/crispy-adventure/_static/ra_media/symmetric_array_pdf(w).png
---
alt: Symmetric Normally Distributed Array
align: center
width: 60%
class: only-dark
---
```

But what I got and moved forward with is this:
```{image} https://abd-01.github.io/crispy-adventure/_static/ra_media/symmetric_array_step.png
---
alt: Symmetric Array
align: center
width: 60%
class: only-light
---
```
```{image} https://abd-01.github.io/crispy-adventure/_static/ra_media/symmetric_array_step(w).png
---
alt: Symmetric Array
align: center
width: 60%
class: only-dark
---
```
````

## References

* Multiple Thresholds for Red: [OpenCV better detection of red color?](https://stackoverflow.com/questions/32522989/opencv-better-detection-of-red-color)
* HSV Ranges: [Identifying the range of a color in HSV using OpenCV](https://stackoverflow.com/questions/36817133/identifying-the-range-of-a-color-in-hsv-using-opencv)
* Centre of a ROI: [Find the Center of a Blob (Centroid) using OpenCV (C++/Python)](https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/)
* Creating symmetric arrays [How to generate a random normal distribution of integers](https://stackoverflow.com/questions/37411633/how-to-generate-a-random-normal-distribution-of-integers)
* PID Tuning: [Ziegler–Nichols method](https://en.wikipedia.org/wiki/Ziegler%E2%80%93Nichols_method)
