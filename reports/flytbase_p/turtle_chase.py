         

          <section class="tex2jax_ignore mathjax_ignore" id="assignment-robotics-engineer">
<h1>Assignment - Robotics Engineer<a class="headerlink" href="#assignment-robotics-engineer" title="Permalink to this heading">#</a></h1>
<p>This report details my work for the Robotics Engineer assignment at <a class="reference external" href="https://www.flytbase.com/">FlytBase</a>.</p>
<p>I implemented a PID controller for goal navigation, incorporated acceleration and deceleration profiles, and enabled grid tracing.</p>
<p>Additionally, I developed circular motion control and a turtle chase with circle fitting for trajectory prediction in the ROS Turtlesim environment.</p>
<section id="modifying-the-turtlesim-window-size">
<h2>Modifying the turtlesim window size<a class="headerlink" href="#modifying-the-turtlesim-window-size" title="Permalink to this heading">#</a></h2>
<p>Default: <code class="docutils literal notranslate"><span class="pre">500x500</span></code> which corresponds to <code class="docutils literal notranslate"><span class="pre">11x11</span></code> unit space. <br />
Required: <code class="docutils literal notranslate"><span class="pre">30x15</span></code> unit space <br />
Solution: <br />
Pixels per unit: ~45 (500 / 11 ≈ 45.45). <br />
Breadth: 30 * 45.45  ≈ 1364 pixels <br />
Height: 15 * 45.45 ≈ 682 pixels</p>
<p>Turtle’s farthest possible co-ordinates:</p>
<div class="highlight-yaml notranslate"><div class="highlight"><pre><span></span><span class="nt">x</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">30.288888931274414</span>
<span class="nt">y</span><span class="p">:</span><span class="w"> </span><span class="l l-Scalar l-Scalar-Plain">15.133333206176758</span>
</pre></div>
</div>
<p>The height was later updated to <code class="docutils literal notranslate"><span class="pre">912</span></code> for goals 4,5 and 6 due to large radii.</p>
</section>
<section id="clamping-linear-and-angular-velocities">
<h2>Clamping Linear and Angular Velocities<a class="headerlink" href="#clamping-linear-and-angular-velocities" title="Permalink to this heading">#</a></h2>
<p>max_linear = 15 <br />
max_angular = 6</p>
<p>This is from trial and error. Initially I choose the maximum values to be 10 and 7 for linear and angular velocities, respectively.</p>
</section>
<section id="spawning-turtle-at-random-location">
<h2>Spawning Turtle at Random Location<a class="headerlink" href="#spawning-turtle-at-random-location" title="Permalink to this heading">#</a></h2>
<p>This can be done using the <a class="reference external" href="https://docs.ros.org/en/noetic/api/turtlesim/html/srv/Spawn.html"><code class="docutils literal notranslate"><span class="pre">spawn</span></code></a> service.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="k">def</span> <span class="nf">spawn_turtle</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">theta</span><span class="o">=</span><span class="mi">0</span><span class="p">):</span>
    <span class="n">rospy</span><span class="o">.</span><span class="n">wait_for_service</span><span class="p">(</span><span class="s1">&#39;/spawn&#39;</span><span class="p">)</span>
    <span class="k">try</span><span class="p">:</span>
        <span class="n">spawn</span> <span class="o">=</span> <span class="n">rospy</span><span class="o">.</span><span class="n">ServiceProxy</span><span class="p">(</span><span class="s1">&#39;/spawn&#39;</span><span class="p">,</span> <span class="n">Spawn</span><span class="p">)</span>
        <span class="n">spawn</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">theta</span><span class="p">,</span> <span class="n">name</span><span class="p">)</span>
    <span class="k">except</span> <span class="n">rospy</span><span class="o">.</span><span class="n">ServiceException</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
        <span class="n">rospy</span><span class="o">.</span><span class="n">loginfo</span><span class="p">(</span><span class="s2">&quot;Service execution failed: </span><span class="si">%s</span><span class="s2">&quot;</span> <span class="o">+</span> <span class="nb">str</span><span class="p">(</span><span class="n">e</span><span class="p">))</span>

<span class="n">spawn_turtle</span><span class="p">(</span><span class="n">t_name</span><span class="p">,</span> <span class="n">random</span><span class="o">.</span><span class="n">uniform</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">30</span><span class="p">),</span> <span class="n">random</span><span class="o">.</span><span class="n">uniform</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">15</span><span class="p">),</span> <span class="n">random</span><span class="o">.</span><span class="n">uniform</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">2</span><span class="o">*</span><span class="n">pi</span><span class="p">))</span>
</pre></div>
</div>
</section>
<section id="pid-controller-goal-1">
<h2>PID Controller (Goal 1)<a class="headerlink" href="#pid-controller-goal-1" title="Permalink to this heading">#</a></h2>
<div class="seealso admonition">
<p class="admonition-title">Wikipedia</p>
<p>A proportional–integral–derivative controller is a feedback-based control loop mechanism commonly used to manage machines and processes that require continuous control and automatic adjustment.</p>
</div>
<a class="reference internal image-reference" href="../../_images/PID-goal-to-goal.gif"><img alt="PID.gif" class="align-center" src="../../_images/PID-goal-to-goal.gif" style="width: 70%;" /></a>
<p>The goal is to get the turtle to the target quickly while avoiding overshoot.</p>
<p>The gains of PID</p>
<ul class="simple">
<li><p>Proportional (Kp): Drives the turtle toward the goal proportional to the error.</p></li>
<li><p>Integral (Ki): Corrects accumulated error over time (for steady-state errors).</p></li>
<li><p>Derivative (Kd): Reduces overshoot by reacting to the rate of error change.</p></li>
</ul>
<p>I need two PID controllers: one for distance (linear velocity) and one for angle (angular velocity).</p>
<p>The continuous-time PID controller equation is:</p>
<div class="math-wrapper docutils container">
<div class="math notranslate nohighlight">
\[
u(t) = K_p \cdot e(t) + K_i \cdot \int e(t) \, dt + K_d \cdot \frac{de(t)}{dt}
\]</div>
</div>
<p>Where:</p>
<ul class="simple">
<li><p><span class="math notranslate nohighlight">\(u(t)\)</span>: Control output.</p></li>
<li><p><span class="math notranslate nohighlight">\(e(t)\)</span>: Error (e.g., distance or angle error).</p></li>
<li><p><span class="math notranslate nohighlight">\(K_p\)</span>, <span class="math notranslate nohighlight">\(K_i\)</span>, <span class="math notranslate nohighlight">\(K_d\)</span>: Proportional, integral, and derivative gains.</p></li>
<li><p><span class="math notranslate nohighlight">\(\int e(t) \, dt\)</span>: Integral of the error over time (accumulates past errors).</p></li>
<li><p><span class="math notranslate nohighlight">\(\frac{de(t)}{dt}\)</span>: Derivative of the error with respect to time (rate of change of error).</p></li>
</ul>
<p>In discrete time, you approximate it as:</p>
<div class="math-wrapper docutils container">
<div class="math notranslate nohighlight">
\[
u(k) = K_p \cdot e(k) + K_i \cdot \sum (e(k) \cdot \Delta t) + K_d \cdot \frac{e(k) - e(k-1)}{\Delta t}
\]</div>
</div>
<p>Where: <span class="math notranslate nohighlight">\(\Delta t\)</span> (or <code class="docutils literal notranslate"><span class="pre">dt</span></code>): Time difference between samples.</p>
<p>Code Implementation:</p>
<div class="highlight-cpp notranslate"><div class="highlight"><pre><span></span><span class="linenos">20</span><span class="k">struct</span><span class="w"> </span><span class="nc">PID</span><span class="w"> </span><span class="p">{</span>
<span class="linenos">21</span><span class="w">    </span><span class="kt">float</span><span class="w"> </span><span class="n">kp</span><span class="p">,</span><span class="w"> </span><span class="n">ki</span><span class="p">,</span><span class="w"> </span><span class="n">kd</span><span class="p">;</span>
<span class="linenos">22</span><span class="w">    </span><span class="kt">float</span><span class="w"> </span><span class="n">error_sum</span><span class="p">;</span>
<span class="linenos">23</span><span class="w">    </span><span class="kt">float</span><span class="w"> </span><span class="n">last_error</span><span class="p">;</span>
<span class="linenos">24</span>
<span class="linenos">25</span><span class="w">    </span><span class="n">PID</span><span class="p">(</span><span class="kt">float</span><span class="w"> </span><span class="n">p</span><span class="p">,</span><span class="w"> </span><span class="kt">float</span><span class="w"> </span><span class="n">i</span><span class="p">,</span><span class="w"> </span><span class="kt">float</span><span class="w"> </span><span class="n">d</span><span class="p">)</span><span class="w"> </span><span class="o">:</span><span class="w"> </span><span class="n">kp</span><span class="p">(</span><span class="n">p</span><span class="p">),</span><span class="w"> </span><span class="n">ki</span><span class="p">(</span><span class="n">i</span><span class="p">),</span><span class="w"> </span><span class="n">kd</span><span class="p">(</span><span class="n">d</span><span class="p">),</span><span class="w"> </span><span class="n">error_sum</span><span class="p">(</span><span class="mf">0.0</span><span class="p">),</span><span class="w"> </span><span class="n">last_error</span><span class="p">(</span><span class="mf">0.0</span><span class="p">)</span><span class="w"> </span><span class="p">{}</span>
<span class="linenos">26</span>
<span class="linenos">27</span><span class="w">    </span><span class="kt">float</span><span class="w"> </span><span class="n">compute</span><span class="p">(</span><span class="kt">float</span><span class="w"> </span><span class="n">error</span><span class="p">,</span><span class="w"> </span><span class="kt">float</span><span class="w"> </span><span class="n">dt</span><span class="p">)</span><span class="w"> </span><span class="p">{</span>
<span class="linenos">28</span><span class="w">        </span><span class="kt">float</span><span class="w"> </span><span class="n">p_term</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">kp</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">error</span><span class="p">;</span>
<span class="linenos">29</span>
<span class="linenos">30</span><span class="w">        </span><span class="n">error_sum</span><span class="w"> </span><span class="o">+=</span><span class="w"> </span><span class="n">error</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">dt</span><span class="p">;</span>
<span class="linenos">31</span><span class="w">        </span><span class="kt">float</span><span class="w"> </span><span class="n">i_term</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">ki</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">error_sum</span><span class="p">;</span>
<span class="linenos">32</span>
<span class="linenos">33</span><span class="w">        </span><span class="kt">float</span><span class="w"> </span><span class="n">derivative</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="p">(</span><span class="n">dt</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span><span class="w"> </span><span class="o">?</span><span class="w"> </span><span class="p">(</span><span class="n">error</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">last_error</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="n">dt</span><span class="w"> </span><span class="o">:</span><span class="w"> </span><span class="mf">0.0f</span><span class="p">;</span>
<span class="linenos">34</span><span class="w">        </span><span class="kt">float</span><span class="w"> </span><span class="n">d_term</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">kd</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">derivative</span><span class="p">;</span>
<span class="linenos">35</span>
<span class="linenos">36</span><span class="w">        </span><span class="n">last_error</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">error</span><span class="p">;</span>
<span class="linenos">37</span>
<span class="linenos">38</span><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="n">p_term</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">i_term</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">d_term</span><span class="p">;</span>
<span class="linenos">39</span><span class="w">    </span><span class="p">}</span>
<span class="linenos">40</span><span class="p">};</span>
</pre></div>
</div>
<section id="tuning-the-pid">
<h3>Tuning the PID<a class="headerlink" href="#tuning-the-pid" title="Permalink to this heading">#</a></h3>
<p>The goal is to get the turtle to target as fast as possible. So the turtle better be facing in the target’s direction as soon as possible.</p>
<p>For this I tuned the controller for angular velocities first.</p>
<p>Started with <span class="math notranslate nohighlight">\(K_p = 1\)</span>, <span class="math notranslate nohighlight">\(K_i = 0\)</span> and <span class="math notranslate nohighlight">\(K_d = 0\)</span>, and then slowly increased <span class="math notranslate nohighlight">\(K_p\)</span> all the way upto <span class="math notranslate nohighlight">\(10\)</span>. The <span class="math notranslate nohighlight">\(K_i\)</span> and <span class="math notranslate nohighlight">\(K_d\)</span> are incresed accordingly depending upon the steady state error and oscillations.</p>
<p>The system goes haywire at around <span class="math notranslate nohighlight">\(K_p = 8\)</span> and above. See the images below.</p>
<!-- Insert PID tuning for angle Part 1 to Part 4 -->
<div class="sd-tab-set docutils">
<input checked="checked" id="sd-tab-item-0" name="sd-tab-set-0" type="radio">
<label class="sd-tab-label" for="sd-tab-item-0">
Slow</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/PID_tuning_angle-Part1.png"><img alt="../../_images/PID_tuning_angle-Part1.png" src="../../_images/PID_tuning_angle-Part1.png" style="width: 100%;" /></a>
</div>
<input id="sd-tab-item-1" name="sd-tab-set-0" type="radio">
<label class="sd-tab-label" for="sd-tab-item-1">
Moderate</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/PID_tuning_angle-Part-2.png"><img alt="../../_images/PID_tuning_angle-Part-2.png" src="../../_images/PID_tuning_angle-Part-2.png" style="width: 100%;" /></a>
</div>
<input id="sd-tab-item-2" name="sd-tab-set-0" type="radio">
<label class="sd-tab-label" for="sd-tab-item-2">
Overshoot</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/PID_tuning_angle-Part-3.png"><img alt="../../_images/PID_tuning_angle-Part-3.png" src="../../_images/PID_tuning_angle-Part-3.png" style="width: 100%;" /></a>
</div>
<input id="sd-tab-item-3" name="sd-tab-set-0" type="radio">
<label class="sd-tab-label" for="sd-tab-item-3">
Unstable</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/PID_tuning_angle-Part-4.png"><img alt="../../_images/PID_tuning_angle-Part-4.png" src="../../_images/PID_tuning_angle-Part-4.png" style="width: 100%;" /></a>
</div>
</div>
<p>In the plots <span class="math notranslate nohighlight">\(K_p=5.0–7.0\)</span> shows fast response but some overshoot, while <span class="math notranslate nohighlight">\(K_p=0.5–2.0\)</span> is too slow. For the oscillation and overshoot I increased the <span class="math notranslate nohighlight">\(K_d\)</span>,. As you can see in the plots <span class="math notranslate nohighlight">\(K_d=0.05\)</span> and <span class="math notranslate nohighlight">\(K_d=0.1\)</span> are working well. Now <span class="math notranslate nohighlight">\(K_i=0\)</span> do leave a slight residual error, so <span class="math notranslate nohighlight">\(K_i=0.01\)</span> worked fine without causing instability.</p>
<p>To have the fastest settling time with minimal overshoot and oscillations, the finalized PID coefficients where
<span class="math notranslate nohighlight">\(K_p=7.0, K_i=0.01, K_d=0.2\)</span></p>
<p>Also, considering linear velocity the angular gains should be stable and settle quickly to avoid interfering with linear motion. The above gains are stable and fast, making it a good choice.</p>
<p>Similarly, for the linear pid, I tested various gains, increasing <span class="math notranslate nohighlight">\(K_p\)</span> and <span class="math notranslate nohighlight">\(K_d\)</span> to get the fastest turtle. Infact, I found out that an unstable turtle with relatively higher <span class="math notranslate nohighlight">\(K_p\)</span> could reach the goal faster that any other except that it will also have a larger overshoot.</p>
<div class="sd-tab-set docutils">
<input id="sd-tab-item-4" name="sd-tab-set-1" type="radio">
<label class="sd-tab-label" for="sd-tab-item-4">
Linear PID</label><div class="sd-tab-content docutils">
<img alt="../../_images/PID_tuning_distance.png" src="../../_images/PID_tuning_distance.png" />
</div>
<input id="sd-tab-item-5" name="sd-tab-set-1" type="radio">
<label class="sd-tab-label" for="sd-tab-item-5">
Goal to Goal (x-component)</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/PID-goal_to_goal-x.png"><img alt="../../_images/PID-goal_to_goal-x.png" class="align-center" src="../../_images/PID-goal_to_goal-x.png" style="width: 90%;" /></a>
</div>
<input id="sd-tab-item-6" name="sd-tab-set-1" type="radio">
<label class="sd-tab-label" for="sd-tab-item-6">
Goal to Goal (y-component)</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/PID-goal_to_goal-y.png"><img alt="../../_images/PID-goal_to_goal-y.png" class="align-center" src="../../_images/PID-goal_to_goal-y.png" style="width: 90%;" /></a>
</div>
<input checked="checked" id="sd-tab-item-7" name="sd-tab-set-1" type="radio">
<label class="sd-tab-label" for="sd-tab-item-7">
Goal to Goal (PlotJuggler)</label><div class="sd-tab-content docutils">
<a href="https://drive.google.com/file/d/162TvkBHGWoKziQULKHKhddyyfgVo7EH1/view" target="_blank">
    <video autoplay="True" loop="True" muted="True" preload="auto" width="100%">
        <source src="https://github.com/user-attachments/assets/fc39544d-1532-4878-bca7-c721d4df9d1b" type="">
    </video>
</a></div>
</div>
<p>The following values were chosen after few iterations for further tuning:</p>
<div class="table-wrapper colwidths-auto docutils container">
<table class="docutils align-default">
<thead>
<tr class="row-odd"><th class="head"><p>Turtle</p></th>
<th class="head"><p>Magenta</p></th>
<th class="head"><p>Violet</p></th>
<th class="head"><p>White</p></th>
<th class="head"><p>Green</p></th>
<th class="head"><p>Blue</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td><p><span class="math notranslate nohighlight">\(K_p\)</span></p></td>
<td><p>0.5</p></td>
<td><p>0.7</p></td>
<td><p>2.0</p></td>
<td><p>2.5</p></td>
<td><p>3.0</p></td>
</tr>
<tr class="row-odd"><td><p><span class="math notranslate nohighlight">\(K_i\)</span></p></td>
<td><p>0.005</p></td>
<td><p>0.05</p></td>
<td><p>0.1</p></td>
<td><p>0.05</p></td>
<td><p>0.01</p></td>
</tr>
<tr class="row-even"><td><p><span class="math notranslate nohighlight">\(K_d\)</span></p></td>
<td><p>0.09</p></td>
<td><p>0.3</p></td>
<td><p>0.9</p></td>
<td><p>0.7</p></td>
<td><p>1.0</p></td>
</tr>
</tbody>
</table>
</div>
<!-- Insert Tuning different PID video -->
<div class="sd-tab-set docutils">
<input checked="checked" id="sd-tab-item-8" name="sd-tab-set-2" type="radio">
<label class="sd-tab-label" for="sd-tab-item-8">
Goal to Goal (Performance with different PID Gains)</label><div class="sd-tab-content docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1XoHNd3Q0iLf-YlBlE1klM0HjqHu8jAOt/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</div>
<p>The blue turtle (turtle3) does appear to win the race each time, however is significantly unstable. The green turtle (turtle2) shows a fast, wide-angle turn, which aligns with its higher speed and aggressive PID settings, while the white turtle (turtle1) has a smoother, more controlled path. The rest two are just slow.</p>
<p>The white turtle (turtle1) is our protagonist meeting Goal 1: fast as possible without overshooting.</p>
</section>
<section id="usage">
<h3>Usage<a class="headerlink" href="#usage" title="Permalink to this heading">#</a></h3>
<div class="highlight-sh notranslate"><div class="highlight"><pre><span></span>$<span class="w"> </span>rosrun<span class="w"> </span>turtlesim<span class="w"> </span>turtlesim_node<span class="w"> </span>
$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_goal_to_goal.py<span class="w"> </span>-x<span class="w"> </span>&lt;goal_x&gt;<span class="w"> </span>-y<span class="w"> </span>&lt;goal_y&gt;
<span class="c1"># example</span>
$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_goal_to_goal.py<span class="w"> </span>-x<span class="w"> </span><span class="m">20</span><span class="w"> </span>-y<span class="w"> </span><span class="m">13</span>
</pre></div>
</div>
<p>To see multiple turtles with different PID gains, call <a class="reference external" href="https://github.com/ABD-01/fluffy-fiesta/blob/master/scripts/turtle_goal_to_goal.py"><code class="docutils literal notranslate"><span class="pre">main_debug()</span></code></a> instead of <code class="docutils literal notranslate"><span class="pre">main()</span></code> function inside the script.</p>
</section>
</section>
<section id="decelerating-turtle-goal-2">
<h2>Decelerating Turtle (Goal 2)<a class="headerlink" href="#decelerating-turtle-goal-2" title="Permalink to this heading">#</a></h2>
<p>The goal is to include realistic deceleration profile for the turtle. Also, move the turtle in a grid.</p>
<p>I have modified <code class="docutils literal notranslate"><span class="pre">PIDTurtleController</span></code> in <a class="reference external" href="https://github.com/ABD-01/fluffy-fiesta/blob/master/scripts/turtle_deceleration.py"><code class="docutils literal notranslate"><span class="pre">turtle_deceleration.py</span></code></a> to impose limitations on maximum acceleration and deceleration.</p>
<section id="implementation-of-deceleration-profiles">
<h3>Implementation of Deceleration Profiles<a class="headerlink" href="#implementation-of-deceleration-profiles" title="Permalink to this heading">#</a></h3>
<p>The code implementation of how I am maintaining the limitations on acceleration and deceleration:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">137</span><span class="n">linear_diff</span> <span class="o">=</span> <span class="n">linear_vel</span> <span class="o">-</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span>
<span class="linenos">138</span><span class="k">if</span><span class="p">(</span><span class="n">linear_diff</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">):</span>  <span class="c1"># Acceleration</span>
<span class="linenos">139</span>    <span class="n">linear_vel</span> <span class="o">=</span> <span class="nb">min</span><span class="p">(</span><span class="n">linear_vel</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span> <span class="o">+</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">max_acc_linear</span> <span class="o">*</span> <span class="mf">0.1</span><span class="p">))</span>
<span class="linenos">140</span><span class="k">else</span><span class="p">:</span>  <span class="c1"># Deceleration</span>
<span class="linenos">141</span>    <span class="n">linear_vel</span> <span class="o">=</span> <span class="nb">max</span><span class="p">(</span><span class="n">linear_vel</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span> <span class="o">-</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">max_dec_linear</span> <span class="o">*</span> <span class="mf">0.1</span><span class="p">))</span>
<span class="linenos">142</span>
<span class="linenos">143</span><span class="n">angular_diff</span> <span class="o">=</span> <span class="n">angular_vel</span> <span class="o">-</span> <span class="bp">self</span><span class="o">.</span><span class="n">angular_vel_old</span>
<span class="linenos">144</span><span class="k">if</span><span class="p">(</span><span class="n">angular_diff</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">):</span>  <span class="c1"># Acceleration</span>
<span class="linenos">145</span>    <span class="n">angular_vel</span> <span class="o">=</span> <span class="nb">min</span><span class="p">(</span><span class="n">angular_vel</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">angular_vel_old</span> <span class="o">+</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">max_acc_angular</span> <span class="o">*</span> <span class="mf">0.1</span><span class="p">))</span>
<span class="linenos">146</span><span class="k">else</span><span class="p">:</span>  <span class="c1"># Deceleration</span>
<span class="linenos">147</span>    <span class="n">angular_vel</span> <span class="o">=</span> <span class="nb">max</span><span class="p">(</span><span class="n">angular_vel</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">angular_vel_old</span> <span class="o">-</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">max_dec_angular</span> <span class="o">*</span> <span class="mf">0.1</span><span class="p">))</span>
</pre></div>
</div>
<p>However, this alone doesn’t ensure turtle decelerates to 0 velocity, when goal is reached, because when goal is reached we previously stop publishing velocity which causes the turtle to stop abruptly.</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">191</span><span class="k">if</span> <span class="n">distance_error</span> <span class="o">&lt;</span> <span class="n">dist_threshold</span> <span class="ow">and</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">:</span>
<span class="linenos">192</span>    <span class="n">rospy</span><span class="o">.</span><span class="n">loginfo</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;[</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">name</span><span class="si">}</span><span class="s2">] Initiating final deceleration to 0...&quot;</span><span class="p">)</span>
<span class="linenos">193</span>    <span class="n">remaining_vel</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span>
<span class="linenos">194</span>    <span class="k">while</span> <span class="n">remaining_vel</span> <span class="o">&gt;</span> <span class="mf">0.1</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">rospy</span><span class="o">.</span><span class="n">is_shutdown</span><span class="p">():</span>
<span class="linenos">195</span>        <span class="n">remaining_vel</span> <span class="o">=</span> <span class="nb">max</span><span class="p">(</span><span class="mf">0.0</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span> <span class="o">-</span> <span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">max_dec_linear</span> <span class="o">*</span> <span class="n">dt</span><span class="p">))</span>
<span class="linenos">196</span>        <span class="n">twist</span> <span class="o">=</span> <span class="n">Twist</span><span class="p">()</span>
<span class="linenos">197</span>        <span class="n">twist</span><span class="o">.</span><span class="n">linear</span><span class="o">.</span><span class="n">x</span> <span class="o">=</span> <span class="n">remaining_vel</span>
<span class="linenos">198</span>        <span class="n">twist</span><span class="o">.</span><span class="n">angular</span><span class="o">.</span><span class="n">z</span> <span class="o">=</span> <span class="mf">0.0</span>  <span class="c1"># No angular motion for straight line</span>
<span class="linenos">199</span>        <span class="bp">self</span><span class="o">.</span><span class="n">vel_pub</span><span class="o">.</span><span class="n">publish</span><span class="p">(</span><span class="n">twist</span><span class="p">)</span>
<span class="linenos">200</span>        <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span> <span class="o">=</span> <span class="n">remaining_vel</span>
<span class="linenos">201</span>        <span class="bp">self</span><span class="o">.</span><span class="n">rate</span><span class="o">.</span><span class="n">sleep</span><span class="p">()</span>
<span class="linenos">202</span>    <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel_old</span> <span class="o">=</span> <span class="mf">0.0</span>  <span class="c1"># Ensure velocity is 0</span>
</pre></div>
</div>
<p>These changes ensure that the turtle’s motion respects maximum acceleration and deceleration limits, preventing abrupt stops and simulating realistic vehicle behavior.</p>
<p>Tested for these different acceleration and deceleration profiles:</p>
<div class="table-wrapper colwidths-auto docutils container">
<table class="docutils align-default">
<thead>
<tr class="row-odd"><th class="head text-center"><p>Max Acceleration</p></th>
<th class="head text-center"><p>Max Deceleration</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td class="text-center"><p>7.5</p></td>
<td class="text-center"><p>7.5</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>15</p></td>
<td class="text-center"><p>15</p></td>
</tr>
<tr class="row-even"><td class="text-center"><p>5</p></td>
<td class="text-center"><p>15</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>15</p></td>
<td class="text-center"><p>5</p></td>
</tr>
</tbody>
</table>
</div>
<section id="pid-gain-adjustments">
<h4>PID Gain Adjustments<a class="headerlink" href="#pid-gain-adjustments" title="Permalink to this heading">#</a></h4>
<p><em>“Check if you need to change the PID gains to accomplish goal 1 once again.”</em></p>
<p>I initially used PID gains from Goal 1 but found it necessary to retune them under the new acceleration/deceleration constraints.
You can see how the tuning was done sequentially in following videos:</p>
<p>Tuning PID gains with Deceleration Profiles:</p>
<div class="sd-tab-set docutils">
<input id="sd-tab-item-9" name="sd-tab-set-3" type="radio">
<label class="sd-tab-label" for="sd-tab-item-9">
Stable (Final Take)</label><div class="sd-tab-content docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1Cq3Z-uBfpxi7ElhwJiTebbV3Yr1Lh0Lj/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
<input id="sd-tab-item-10" name="sd-tab-set-3" type="radio">
<label class="sd-tab-label" for="sd-tab-item-10">
Almost Good</label><div class="sd-tab-content docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1DSYCwDLSVQufEgY9GkbC9FRVxsRyny4C/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
<input id="sd-tab-item-11" name="sd-tab-set-3" type="radio">
<label class="sd-tab-label" for="sd-tab-item-11">
Unstable</label><div class="sd-tab-content docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1YYHLeKtiz3-gNtmtRWgeHV-k8xT4Erhf/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
<input checked="checked" id="sd-tab-item-12" name="sd-tab-set-3" type="radio">
<label class="sd-tab-label" for="sd-tab-item-12">
Chaos</label><div class="sd-tab-content docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1gOCPIl7waSx_kiYVmIvfmEPAy9_T8Hby/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</div>
<p><em>“Do you need to change gains every time? If yes/no, why?”</em></p>
<p>These gains were adjusted to ensure stable, fast motion while respecting acceleration/deceleration limits. There was no not need to retune the gains for every acceleration profile, as the changes primarily affected the velocity limits rather than the PID dynamics. The retuning was necessary mainly due to large <span class="math notranslate nohighlight">\(K_p\)</span> in Goal 1 causing the velocity to hit the maximum, while acceleration holding it down. The tuning was one time to balance the slower response caused by deceleration limits, ensuring the turtle still reaches goals quickly without oscillations.</p>
<p>The finalized parameters after testing and tuning are:</p>
<div class="table-wrapper colwidths-auto docutils container">
<table class="docutils align-default" style="width: 100%">
<thead>
<tr class="row-odd"><th class="head text-center"><p>Parameter</p></th>
<th class="head text-center"><p>Value</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td class="text-center"><p>Distance PID <span class="math notranslate nohighlight">\(K_p\)</span></p></td>
<td class="text-center"><p>0.70</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>Distance PID <span class="math notranslate nohighlight">\(K_i\)</span></p></td>
<td class="text-center"><p>0.05</p></td>
</tr>
<tr class="row-even"><td class="text-center"><p>Distance PID <span class="math notranslate nohighlight">\(K_d\)</span></p></td>
<td class="text-center"><p>0.30</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>Angular PID <span class="math notranslate nohighlight">\(K_p\)</span></p></td>
<td class="text-center"><p>5.00</p></td>
</tr>
<tr class="row-even"><td class="text-center"><p>Angular PID <span class="math notranslate nohighlight">\(K_i\)</span></p></td>
<td class="text-center"><p>0.01</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>Angular PID <span class="math notranslate nohighlight">\(K_d\)</span></p></td>
<td class="text-center"><p>0.70</p></td>
</tr>
<tr class="row-even"><td class="text-center"><p>Max Linear Acc</p></td>
<td class="text-center"><p>7.00</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>Max Linear Dec</p></td>
<td class="text-center"><p>7.50</p></td>
</tr>
<tr class="row-even"><td class="text-center"><p>Max Angular Acc</p></td>
<td class="text-center"><p>5.80</p></td>
</tr>
<tr class="row-odd"><td class="text-center"><p>Max Angular Dec</p></td>
<td class="text-center"><p>5.80</p></td>
</tr>
</tbody>
</table>
</div>
<div class="tip admonition">
<p class="admonition-title">Note</p>
<p>These values the fixed for the rest of the assignments. The turtle in the next goals will be using these same values. This is because the assignment says <em>“It is expected that all the above cases are passed by the same code/logic, without modification of any other parameters except the 3 defined above.”</em></p>
</div>
</section>
<section id="id1">
<h4>Usage<a class="headerlink" href="#id1" title="Permalink to this heading">#</a></h4>
<div class="highlight-sh notranslate"><div class="highlight"><pre><span></span>rosrun<span class="w"> </span>turtlesim<span class="w"> </span>turtlesim_node<span class="w"> </span>
rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_deceleration.py<span class="w"> </span>-x<span class="w"> </span><span class="m">20</span><span class="w"> </span>-y<span class="w"> </span><span class="m">13</span>
</pre></div>
</div>
<p>To see multiple turtles with different acceleration profiles, call <code class="docutils literal notranslate"><span class="pre">main_debug()</span></code> instead of <code class="docutils literal notranslate"><span class="pre">main()</span></code> function inside the script.</p>
</section>
</section>
<section id="tracing-the-grid">
<h3>Tracing the Grid<a class="headerlink" href="#tracing-the-grid" title="Permalink to this heading">#</a></h3>
<div class="sd-tab-set docutils">
<input checked="checked" id="sd-tab-item-13" name="sd-tab-set-4" type="radio">
<label class="sd-tab-label" for="sd-tab-item-13">
Turtlesim Grid</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/grid-turtle.png"><img alt="../../_images/grid-turtle.png" class="align-center" src="../../_images/grid-turtle.png" style="width: 90%;" /></a>
</div>
<input id="sd-tab-item-14" name="sd-tab-set-4" type="radio">
<label class="sd-tab-label" for="sd-tab-item-14">
PlotJuggler</label><div class="sd-tab-content docutils">
<a class="reference internal image-reference" href="../../_images/Grid.png"><img alt="../../_images/Grid.png" src="../../_images/Grid.png" style="width: 100%;" /></a>
</div>
</div>
<p>I implemented two motion control strategies in the <code class="docutils literal notranslate"><span class="pre">pub_vel</span></code> function to manage linear and angular velocities, impacting the grid pattern’s stability and efficiency:</p>
<p><strong>Stop and Rotate, Then Move Forward</strong>:</p>
<ul class="simple">
<li><p>The turtle first rotates in place to face the goal (using only angular velocity) until its heading aligns with the goal direction.</p></li>
<li><p>Once aligned, it moves forward (using only linear velocity) until reaching the goal.</p></li>
</ul>
<p><strong>Update Linear and Angular Velocities Simultaneously</strong>:</p>
<ul class="simple">
<li><p>The turtle adjusts both linear and angular velocities concurrently using independent PID controllers for distance (linear velocity) and angle (angular velocity).</p></li>
</ul>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">126</span>        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">rotate_first</span><span class="p">:</span>
<span class="linenos">127</span>            <span class="c1"># Prioritize rotaton by limitng velocity</span>
<span class="linenos">128</span>            <span class="k">if</span> <span class="nb">abs</span><span class="p">(</span><span class="n">angle_error</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mf">0.1</span><span class="p">:</span>
<span class="linenos">129</span>                <span class="n">linear_vel</span> <span class="o">*=</span> <span class="mf">0.05</span>
<span class="linenos">130</span>        <span class="k">else</span><span class="p">:</span>
<span class="linenos">131</span>            <span class="c1"># limit velocity on sharp turn</span>
<span class="linenos">132</span>            <span class="k">if</span> <span class="nb">abs</span><span class="p">(</span><span class="n">angle_error</span><span class="p">)</span> <span class="o">&gt;</span> <span class="n">pi</span> <span class="o">/</span> <span class="mi">2</span><span class="p">:</span>
<span class="linenos">133</span>                <span class="n">linear_vel</span> <span class="o">*=</span> <span class="mf">0.7</span>
<span class="linenos">134</span>
</pre></div>
</div>
<p>I have used simultaneous update strategy everywhere, but for the grid solution used the stop-and-rotate option for stability in rotation.</p>
<!-- Insert Grid videos -->
<p>Here’s the video of turtle following the grid pattern:</p>
<div width="90%" align="center">
<iframe src="https://drive.google.com/file/d/1szmsnSR37P7CqoCXxNfUrW7wOx02XvAg/preview" width="640" height="480" allow="autoplay"></iframe>
</div><section id="id2">
<h4>Usage<a class="headerlink" href="#id2" title="Permalink to this heading">#</a></h4>
<div class="highlight-sh notranslate"><div class="highlight"><pre><span></span>roslaunch<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_grid.launch
</pre></div>
</div>
</section>
</section>
</section>
<section id="circular-motion-of-the-turtle-goal-3">
<h2>Circular Motion of the Turtle (Goal 3)<a class="headerlink" href="#circular-motion-of-the-turtle-goal-3" title="Permalink to this heading">#</a></h2>
<p>To move in a circle, the turtle needs a constant linear velocity (<span class="math notranslate nohighlight">\(v\)</span>) and a constant angular velocity (<span class="math notranslate nohighlight">\(\omega\)</span>). The radius (<span class="math notranslate nohighlight">\(r\)</span>) of the circle is determined by <span class="math notranslate nohighlight">\(r = v/\omega\)</span></p>
<p>The code for this goal includes the following logic:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos"> 86</span><span class="k">def</span> <span class="nf">move_in_circle</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
<span class="linenos"> 87</span>    <span class="k">while</span> <span class="ow">not</span> <span class="n">rospy</span><span class="o">.</span><span class="n">is_shutdown</span><span class="p">():</span>
<span class="linenos"> 88</span>        <span class="bp">self</span><span class="o">.</span><span class="n">angular_vel</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">linear_vel</span> <span class="o">/</span> <span class="bp">self</span><span class="o">.</span><span class="n">radius</span>
<span class="linenos"> 89</span>        <span class="bp">self</span><span class="o">.</span><span class="n">pub_vel</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">linear_vel</span><span class="p">,</span> <span class="bp">self</span><span class="o">.</span><span class="n">angular_vel</span><span class="p">)</span>
<span class="linenos"> 90</span>
<span class="linenos"> 91</span>        <span class="c1"># Publish pose every 5 seconds</span>
<span class="linenos"> 92</span>        <span class="n">current_time</span> <span class="o">=</span> <span class="n">rospy</span><span class="o">.</span><span class="n">get_time</span><span class="p">()</span>
<span class="linenos"> 93</span>        <span class="k">if</span> <span class="n">current_time</span> <span class="o">-</span> <span class="bp">self</span><span class="o">.</span><span class="n">last_publish_time</span> <span class="o">&gt;=</span> <span class="mf">5.0</span><span class="p">:</span>
<span class="linenos"> 94</span>            <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">current_pose</span><span class="p">:</span>
<span class="linenos"> 95</span>                <span class="c1"># Publish real pose</span>
<span class="linenos"> 96</span>                <span class="n">real_pose</span> <span class="o">=</span> <span class="n">Pose</span><span class="p">()</span>
<span class="linenos"> 97</span>                <span class="n">real_pose</span><span class="o">.</span><span class="n">x</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">current_pose</span><span class="o">.</span><span class="n">x</span>
<span class="linenos"> 98</span>                <span class="n">real_pose</span><span class="o">.</span><span class="n">y</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">current_pose</span><span class="o">.</span><span class="n">y</span>
<span class="linenos"> 99</span>                <span class="n">real_pose</span><span class="o">.</span><span class="n">theta</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">current_pose</span><span class="o">.</span><span class="n">theta</span>
<span class="linenos">100</span>                <span class="bp">self</span><span class="o">.</span><span class="n">real_pose_pub</span><span class="o">.</span><span class="n">publish</span><span class="p">(</span><span class="n">real_pose</span><span class="p">)</span>
<span class="linenos">101</span>
<span class="linenos">102</span>                <span class="c1"># Publish noisy pose</span>
<span class="linenos">103</span>                <span class="n">noisy_pose</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">add_noise</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">current_pose</span><span class="p">)</span>
<span class="linenos">104</span>                <span class="bp">self</span><span class="o">.</span><span class="n">noisy_pose_pub</span><span class="o">.</span><span class="n">publish</span><span class="p">(</span><span class="n">noisy_pose</span><span class="p">)</span>
<span class="linenos">105</span>
<span class="linenos">106</span>            <span class="bp">self</span><span class="o">.</span><span class="n">last_publish_time</span> <span class="o">=</span> <span class="n">current_time</span>
<span class="linenos">107</span>
<span class="linenos">108</span>        <span class="bp">self</span><span class="o">.</span><span class="n">rate</span><span class="o">.</span><span class="n">sleep</span><span class="p">()</span>
</pre></div>
</div>
<p><strong>Usage</strong></p>
<div class="highlight-bash notranslate"><div class="highlight"><pre><span></span>$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_circle.py<span class="w"> </span>-h
usage:<span class="w"> </span>turtle_circle.py<span class="w"> </span><span class="o">[</span>-h<span class="o">]</span><span class="w"> </span><span class="o">[</span>-s<span class="w"> </span>SPEED<span class="o">]</span><span class="w"> </span><span class="o">[</span>-r<span class="w"> </span>RADIUS<span class="o">]</span>

Move<span class="w"> </span>TurtleSim<span class="w"> </span>turtle<span class="w"> </span><span class="k">in</span><span class="w"> </span>circles

optional<span class="w"> </span>arguments:
<span class="w">  </span>-h,<span class="w"> </span>--help<span class="w">            </span>show<span class="w"> </span>this<span class="w"> </span><span class="nb">help</span><span class="w"> </span>message<span class="w"> </span>and<span class="w"> </span><span class="nb">exit</span>
<span class="w">  </span>-s<span class="w"> </span>SPEED,<span class="w"> </span>--speed<span class="w"> </span>SPEED
<span class="w">                        </span>Linear<span class="w"> </span>speed<span class="w"> </span><span class="o">(</span>units/s<span class="o">)</span>
<span class="w">  </span>-r<span class="w"> </span>RADIUS,<span class="w"> </span>--radius<span class="w"> </span>RADIUS
<span class="w">                        </span>Radius<span class="w"> </span>of<span class="w"> </span>the<span class="w"> </span>circle<span class="w"> </span><span class="o">(</span>units<span class="o">)</span>
<span class="w">                        </span>
<span class="c1"># example</span>
$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_circle.py<span class="w"> </span>-s<span class="w"> </span><span class="m">12</span><span class="w"> </span>-r<span class="w"> </span><span class="m">5</span>
</pre></div>
</div>
</section>
<section id="the-turtle-chase-goals-4-5-6">
<h2>The Turtle Chase (Goals 4,5,6)<a class="headerlink" href="#the-turtle-chase-goals-4-5-6" title="Permalink to this heading">#</a></h2>
<p>Since Police Turtle (PT) do not have real time information of the Robber Turtle’s (RT) pose, I am predicting where the RT will be in next <span class="math notranslate nohighlight">\(t\)</span> seconds (<span class="math notranslate nohighlight">\(t=5\)</span> default) and feed that a target position to the PT.</p>
<p>Judging the caught condition with an outdated pose (up to 5 seconds old) is problematic. Adding a time check (e.g., only consider RT caught if the last pose was received within the last t=1 second) help ensure the pose is recent enough to be meaningful.</p>
<p>Now the above logic works for Goal 4 as the speed of PT is greater than speed of RT, hence it can cover the required distance within the <span class="math notranslate nohighlight">\(5\)</span> seconds.</p>
<p>However, for slower PT, instead of predicting the position of RT once, I generate a series of future positions of RT for <span class="math notranslate nohighlight">\(t = 5, 10, 15, .., 30\)</span> seconds. For each predicted position, check if PT can reach there before RT, and then selects the earliest reachable point as the goal.</p>
<section id="predicting-future-position">
<h3>Predicting Future Position<a class="headerlink" href="#predicting-future-position" title="Permalink to this heading">#</a></h3>
<p>See my notes below from a course.
To predict the next pose of a turtle at a future time <span class="math notranslate nohighlight">\(t + \Delta t\)</span>, given its current pose <span class="math notranslate nohighlight">\((x,y,\theta,v,\omega)\)</span> at time <span class="math notranslate nohighlight">\(t\)</span>, we can use a simple kinematic model of a unicycle.</p>
<details open>
<!-- insert Notes's PDF-->
<summary>Control for Unicycle Robot</summary>
<p><img alt="" src="../../_images/Control_for_Unicycle_Robot_1.jpg" />
<img alt="" src="../../_images/Control_for_Unicycle_Robot_2.jpg" /></p>
</details>
<p>The corresponding code:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">176</span><span class="k">def</span> <span class="nf">predict_rt_pose</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">pose</span><span class="p">,</span> <span class="n">dtime</span><span class="o">=</span><span class="mi">5</span><span class="p">):</span>
<span class="linenos">177</span>    <span class="k">if</span> <span class="n">pose</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
<span class="linenos">178</span>        <span class="k">return</span> <span class="kc">None</span><span class="p">,</span> <span class="kc">None</span><span class="p">,</span> <span class="kc">None</span>
<span class="linenos">179</span>    <span class="n">v</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">linear_velocity</span>
<span class="linenos">180</span>    <span class="n">w</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">angular_velocity</span>
<span class="linenos">181</span>    
<span class="linenos">182</span>    <span class="n">theta</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">theta</span> <span class="o">+</span> <span class="n">w</span> <span class="o">*</span> <span class="n">dtime</span> 
<span class="linenos">183</span>    <span class="k">if</span> <span class="nb">abs</span><span class="p">(</span><span class="n">w</span><span class="p">)</span> <span class="o">&lt;</span> <span class="mf">1e-6</span><span class="p">:</span>
<span class="linenos">184</span>        <span class="n">x</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">x</span> <span class="o">+</span> <span class="n">v</span> <span class="o">*</span> <span class="n">dtime</span> <span class="o">*</span> <span class="n">cos</span><span class="p">(</span><span class="n">pose</span><span class="o">.</span><span class="n">theta</span><span class="p">)</span>
<span class="linenos">185</span>        <span class="n">y</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">y</span> <span class="o">+</span> <span class="n">v</span> <span class="o">*</span> <span class="n">dtime</span> <span class="o">*</span> <span class="n">sin</span><span class="p">(</span><span class="n">pose</span><span class="o">.</span><span class="n">theta</span><span class="p">)</span>
<span class="linenos">186</span>        <span class="k">return</span> <span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">theta</span><span class="p">)</span>
<span class="linenos">187</span>        
<span class="linenos">188</span>    <span class="n">r</span> <span class="o">=</span> <span class="n">v</span> <span class="o">/</span> <span class="n">w</span> <span class="c1"># above condition prevent divide by 0</span>
<span class="linenos">189</span>    <span class="n">x</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">x</span> <span class="o">+</span> <span class="n">r</span> <span class="o">*</span> <span class="p">(</span><span class="n">sin</span><span class="p">(</span><span class="n">pose</span><span class="o">.</span><span class="n">theta</span> <span class="o">+</span> <span class="n">w</span> <span class="o">*</span> <span class="n">dtime</span><span class="p">)</span> <span class="o">-</span> <span class="n">sin</span><span class="p">(</span><span class="n">pose</span><span class="o">.</span><span class="n">theta</span><span class="p">))</span>
<span class="linenos">190</span>    <span class="n">y</span> <span class="o">=</span> <span class="n">pose</span><span class="o">.</span><span class="n">y</span> <span class="o">-</span> <span class="n">r</span> <span class="o">*</span> <span class="p">(</span><span class="n">cos</span><span class="p">(</span><span class="n">pose</span><span class="o">.</span><span class="n">theta</span> <span class="o">+</span> <span class="n">w</span> <span class="o">*</span> <span class="n">dtime</span><span class="p">)</span> <span class="o">-</span> <span class="n">cos</span><span class="p">(</span><span class="n">pose</span><span class="o">.</span><span class="n">theta</span><span class="p">))</span>
<span class="linenos">191</span>    <span class="n">rospy</span><span class="o">.</span><span class="n">logdebug</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;RT will go from (</span><span class="si">{</span><span class="n">pose</span><span class="o">.</span><span class="n">x</span><span class="si">}</span><span class="s2">, </span><span class="si">{</span><span class="n">pose</span><span class="o">.</span><span class="n">y</span><span class="si">}</span><span class="s2">) to (</span><span class="si">{</span><span class="n">x</span><span class="si">}</span><span class="s2">, </span><span class="si">{</span><span class="n">y</span><span class="si">}</span><span class="s2">) in </span><span class="si">{</span><span class="n">dtime</span><span class="si">}</span><span class="s2"> seconds&quot;</span><span class="p">)</span>
<span class="linenos">192</span>    <span class="k">return</span> <span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">,</span> <span class="n">theta</span><span class="p">)</span>
</pre></div>
</div>
</section>
<section id="circle-fitting-for-rt-trajectory">
<h3>Circle Fitting for RT Trajectory<a class="headerlink" href="#circle-fitting-for-rt-trajectory" title="Permalink to this heading">#</a></h3>
<p>Since, the assignment says
<em>“The PT cannot “assume” that the RT is moving in a circle. The PT has to deduce the RT is moving in a circle, the center of the circle, and the radius of the circle.”</em></p>
<p><strong>Logic:</strong></p>
<ul class="simple">
<li><p>To fit a circle from observed RT positions, at least three points are needed.</p></li>
<li><p>The more data points are available the accurate the circle prediction will be. I am starting the after getting at least 5 data points.</p></li>
<li><p>I use the Kåsa fitting algorithm, which uses algebraic least squares to fit a circle to the data points. (See my notes below that explains the algorithm.)</p></li>
</ul>
<!-- Insert my notes -->
<details>
<summary>Circle Fitting Notes</summary>
<p><img alt="" src="../../_images/Circle_Fitting_1.jpg" />
<img alt="" src="../../_images/Circle_Fitting_2.jpg" /></p>
</details>
<p>Implementation:</p>
<div class="highlight-python notranslate"><div class="highlight"><pre><span></span><span class="linenos">148</span><span class="k">def</span> <span class="nf">fit_circle</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">x</span><span class="p">,</span> <span class="n">y</span><span class="p">):</span>
<span class="linenos">149</span>    <span class="n">x</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">x</span><span class="p">)</span>
<span class="linenos">150</span>    <span class="n">y</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">y</span><span class="p">)</span>
<span class="linenos">151</span>    <span class="n">N</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">x</span><span class="p">)</span>
<span class="linenos">152</span>
<span class="linenos">153</span>    <span class="c1"># Build matrix and vector</span>
<span class="linenos">154</span>    <span class="n">A</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span>
<span class="linenos">155</span>        <span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span><span class="o">**</span><span class="mi">2</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span><span class="o">*</span><span class="n">y</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span><span class="p">)],</span>
<span class="linenos">156</span>        <span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span><span class="o">*</span><span class="n">y</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">y</span><span class="o">**</span><span class="mi">2</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">y</span><span class="p">)],</span>
<span class="linenos">157</span>        <span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">y</span><span class="p">),</span> <span class="n">N</span><span class="p">]</span>
<span class="linenos">158</span>    <span class="p">])</span>
<span class="linenos">159</span>    <span class="n">b</span> <span class="o">=</span> <span class="o">-</span><span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span>
<span class="linenos">160</span>        <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span> <span class="o">*</span> <span class="p">(</span><span class="n">x</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="n">y</span><span class="o">**</span><span class="mi">2</span><span class="p">)),</span>
<span class="linenos">161</span>        <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">y</span> <span class="o">*</span> <span class="p">(</span><span class="n">x</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="n">y</span><span class="o">**</span><span class="mi">2</span><span class="p">)),</span>
<span class="linenos">162</span>        <span class="n">np</span><span class="o">.</span><span class="n">sum</span><span class="p">(</span><span class="n">x</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="n">y</span><span class="o">**</span><span class="mi">2</span><span class="p">)</span>
<span class="linenos">163</span>    <span class="p">])</span>
<span class="linenos">164</span>
<span class="linenos">165</span>    <span class="c1"># Solve A * [D, E, F] = b</span>
<span class="linenos">166</span>    <span class="n">D</span><span class="p">,</span> <span class="n">E</span><span class="p">,</span> <span class="n">F</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">solve</span><span class="p">(</span><span class="n">A</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>
<span class="linenos">167</span>
<span class="linenos">168</span>    <span class="c1"># Convert to circle parameters</span>
<span class="linenos">169</span>    <span class="n">a</span> <span class="o">=</span> <span class="o">-</span><span class="n">D</span> <span class="o">/</span> <span class="mi">2</span>
<span class="linenos">170</span>    <span class="n">b</span> <span class="o">=</span> <span class="o">-</span><span class="n">E</span> <span class="o">/</span> <span class="mi">2</span>
<span class="linenos">171</span>    <span class="n">r</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">sqrt</span><span class="p">(</span><span class="n">a</span><span class="o">**</span><span class="mi">2</span> <span class="o">+</span> <span class="n">b</span><span class="o">**</span><span class="mi">2</span> <span class="o">-</span> <span class="n">F</span><span class="p">)</span>
<span class="linenos">172</span>
<span class="linenos">173</span>    <span class="n">rospy</span><span class="o">.</span><span class="n">loginfo</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;[Fitcircle] Center: (</span><span class="si">{</span><span class="n">a</span><span class="si">:</span><span class="s2">.2f</span><span class="si">}</span><span class="s2">, </span><span class="si">{</span><span class="n">b</span><span class="si">:</span><span class="s2">.2f</span><span class="si">}</span><span class="s2">), Radius: </span><span class="si">{</span><span class="n">r</span><span class="si">:</span><span class="s2">.2f</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
<span class="linenos">174</span>    <span class="k">return</span> <span class="n">a</span><span class="p">,</span><span class="n">b</span><span class="p">,</span><span class="n">r</span>
</pre></div>
</div>
<p>PT collects poses over time and fits a circle, updating its prediction model.</p>
</section>
<section id="id3">
<h3>Usage<a class="headerlink" href="#id3" title="Permalink to this heading">#</a></h3>
<div class="highlight-sh notranslate"><div class="highlight"><pre><span></span>$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_fit_circle_chase.py<span class="w"> </span>-h
usage:<span class="w"> </span>turtle_fit_circle_chase.py<span class="w"> </span><span class="o">[</span>-h<span class="o">]</span><span class="w"> </span><span class="o">[</span>-s<span class="w"> </span>RT_SPEED<span class="o">]</span><span class="w"> </span><span class="o">[</span>-p<span class="w"> </span>PT_SPEED<span class="o">]</span><span class="w"> </span><span class="o">[</span>-r<span class="w"> </span>RADIUS<span class="o">]</span><span class="w"> </span><span class="o">[</span>--noisy<span class="o">]</span>

Move<span class="w"> </span>TurtleSim<span class="w"> </span>turtle<span class="w"> </span><span class="k">in</span><span class="w"> </span>circles

optional<span class="w"> </span>arguments:
<span class="w">  </span>-h,<span class="w"> </span>--help<span class="w">            </span>show<span class="w"> </span>this<span class="w"> </span><span class="nb">help</span><span class="w"> </span>message<span class="w"> </span>and<span class="w"> </span><span class="nb">exit</span>
<span class="w">  </span>-s<span class="w"> </span>RT_SPEED,<span class="w"> </span>--rt_speed<span class="w"> </span>RT_SPEED
<span class="w">                        </span>Linear<span class="w"> </span>speed<span class="w"> </span><span class="k">for</span><span class="w"> </span>Robber<span class="w"> </span>Turtle
<span class="w">  </span>-p<span class="w"> </span>PT_SPEED,<span class="w"> </span>--pt_speed<span class="w"> </span>PT_SPEED
<span class="w">                        </span>Linear<span class="w"> </span>speed<span class="w"> </span><span class="k">for</span><span class="w"> </span>Police<span class="w"> </span>Turtle
<span class="w">  </span>-r<span class="w"> </span>RADIUS,<span class="w"> </span>--radius<span class="w"> </span>RADIUS
<span class="w">                        </span>Radius<span class="w"> </span>of<span class="w"> </span>the<span class="w"> </span>circle<span class="w"> </span><span class="k">for</span><span class="w"> </span>Robber<span class="w"> </span>Turtle
<span class="w">  </span>--noisy<span class="w">               </span>Use<span class="w"> </span>/rt_noisy_pose<span class="w"> </span>instead<span class="w"> </span>of<span class="w"> </span>/rt_real_pose

<span class="c1"># example</span>
$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_fit_circle_chase.py<span class="w"> </span>-p<span class="w"> </span><span class="m">3</span>.5<span class="w"> </span>-s<span class="w"> </span><span class="m">1</span><span class="w"> </span>-r<span class="w"> </span><span class="m">6</span>
<span class="c1"># can also try using `turtle_chase.py` for Goal 4 (logic was later updated file kept for legacy)</span>
$<span class="w"> </span>rosrun<span class="w"> </span>flytbase_assignment<span class="w"> </span>turtle_chase.py<span class="w"> </span>-p<span class="w"> </span><span class="m">3</span>.5<span class="w"> </span>-s<span class="w"> </span><span class="m">1</span><span class="w"> </span>-r<span class="w"> </span><span class="m">6</span>
</pre></div>
</div>
</section>
<section id="fast-chase">
<h3>Fast Chase<a class="headerlink" href="#fast-chase" title="Permalink to this heading">#</a></h3>
<p>Following are the videos of PT chasing RT, where speed of PT is greater tha speed of RT.</p>
<details class="sd-sphinx-override sd-dropdown sd-card sd-mb-3 sd-fade-in-slide-down">
<summary class="sd-summary-title sd-card-header">
<span class="sd-summary-text"><span class="math notranslate nohighlight">\(\text{PT}_{\text{Speed}} = 1.2\)</span>, <span class="math notranslate nohighlight">\(\text{RT}_{\text{Speed}} = 1\)</span>, <span class="math notranslate nohighlight">\(\text{Radius} = 9\)</span></span><span class="sd-summary-state-marker sd-summary-chevron-down"><svg version="1.1" width="1.5em" height="1.5em" class="sd-octicon sd-octicon-chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"></path></svg></span></summary><div class="sd-summary-content sd-card-body docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1qqM6O1l-y_VJLw_ZDSROguVF8YDp8KkV/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</details><details class="sd-sphinx-override sd-dropdown sd-card sd-mb-3 sd-fade-in-slide-down">
<summary class="sd-summary-title sd-card-header">
<span class="sd-summary-text"><span class="math notranslate nohighlight">\(\text{PT}_{\text{Speed}} = 2\)</span>, <span class="math notranslate nohighlight">\(\text{RT}_{\text{Speed}} = 1\)</span>, <span class="math notranslate nohighlight">\(\text{Radius} = 8\)</span></span><span class="sd-summary-state-marker sd-summary-chevron-down"><svg version="1.1" width="1.5em" height="1.5em" class="sd-octicon sd-octicon-chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"></path></svg></span></summary><div class="sd-summary-content sd-card-body docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1aLg8Cf5lV31oKWQ-uwH4SxK9krtdiE_1/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</details><details class="sd-sphinx-override sd-dropdown sd-card sd-mb-3 sd-fade-in-slide-down" open="open">
<summary class="sd-summary-title sd-card-header">
<span class="sd-summary-text"><span class="math notranslate nohighlight">\(\text{PT}_{\text{Speed}} = 3.5\)</span>, <span class="math notranslate nohighlight">\(\text{RT}_{\text{Speed}} = 1\)</span>, <span class="math notranslate nohighlight">\(\text{Radius} = 6\)</span></span><span class="sd-summary-state-marker sd-summary-chevron-down"><svg version="1.1" width="1.5em" height="1.5em" class="sd-octicon sd-octicon-chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"></path></svg></span></summary><div class="sd-summary-content sd-card-body docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1GifSFODIxmRlTpqoMFid_QeSXB191XVE/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</details><details class="sd-sphinx-override sd-dropdown sd-card sd-mb-3 sd-fade-in-slide-down">
<summary class="sd-summary-title sd-card-header">
<span class="sd-summary-text"><span class="math notranslate nohighlight">\(\text{PT}_{\text{Speed}} = 4\)</span>, <span class="math notranslate nohighlight">\(\text{RT}_{\text{Speed}} = 2\)</span>, <span class="math notranslate nohighlight">\(\text{Radius} = 5\)</span></span><span class="sd-summary-state-marker sd-summary-chevron-down"><svg version="1.1" width="1.5em" height="1.5em" class="sd-octicon sd-octicon-chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"></path></svg></span></summary><div class="sd-summary-content sd-card-body docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/171zPNEviTx9gGuMWObxXcL3bHjy7wxTG/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</details><details class="sd-sphinx-override sd-dropdown sd-card sd-mb-3 sd-fade-in-slide-down">
<summary class="sd-summary-title sd-card-header">
<span class="sd-summary-text"><span class="math notranslate nohighlight">\(\text{PT}_{\text{Speed}} = 6\)</span>, <span class="math notranslate nohighlight">\(\text{RT}_{\text{Speed}} = 1\)</span>, <span class="math notranslate nohighlight">\(\text{Radius} = 3\)</span></span><span class="sd-summary-state-marker sd-summary-chevron-down"><svg version="1.1" width="1.5em" height="1.5em" class="sd-octicon sd-octicon-chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"></path></svg></span></summary><div class="sd-summary-content sd-card-body docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/1uIp5ToNPUCo0B0922VQNsvI5rzq-R9rY/preview" width="640" height="480" allow="autoplay"></iframe>
</div></div>
</details></section>
<section id="slow-chase">
<h3>Slow Chase<a class="headerlink" href="#slow-chase" title="Permalink to this heading">#</a></h3>
<p>Following is the video of PT chasing RT, where speed of PT is less than speed of RT.</p>
<details class="sd-sphinx-override sd-dropdown sd-card sd-mb-3 sd-fade-in-slide-down" open="open">
<summary class="sd-summary-title sd-card-header">
<span class="sd-summary-text">Goal 5</span><span class="sd-summary-state-marker sd-summary-chevron-down"><svg version="1.1" width="1.5em" height="1.5em" class="sd-octicon sd-octicon-chevron-down" viewBox="0 0 24 24" aria-hidden="true"><path d="M5.22 8.22a.749.749 0 0 0 0 1.06l6.25 6.25a.749.749 0 0 0 1.06 0l6.25-6.25a.749.749 0 1 0-1.06-1.06L12 13.939 6.28 8.22a.749.749 0 0 0-1.06 0Z"></path></svg></span></summary><div class="sd-summary-content sd-card-body docutils">
<div width="100%" align="center">
<iframe src="https://drive.google.com/file/d/10coEcFjDmWnJORHawuKjOwwb5QNG3hFY/preview" width="640" height="480" allow="autoplay"></iframe>
</div>

<ul class="fa-ul">
  <li data-marker="+"><p class="sd-card-text">The subsection are at the mentioned timestamps.</p>
    <ul>
      <li data-marker="*"><p class="sd-card-text"><span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="65" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c50"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>PT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="66" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c30"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c35"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>0.5</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="67" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>RT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="68" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c31"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1.2</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="69" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c61"></mjx-c><mjx-c class="mjx-c64"></mjx-c><mjx-c class="mjx-c69"></mjx-c><mjx-c class="mjx-c75"></mjx-c><mjx-c class="mjx-c73"></mjx-c></mjx-mtext></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mtext>Radius</mtext></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="70" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c39"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>9</mn></math></mjx-assistive-mml></mjx-container></span> at 0:09</p></li>
      <li data-marker="*"><p class="sd-card-text"><span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="71" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c50"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>PT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="72" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c30"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c38"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>0.8</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="73" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>RT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="74" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c31"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c36"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1.6</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="75" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c61"></mjx-c><mjx-c class="mjx-c64"></mjx-c><mjx-c class="mjx-c69"></mjx-c><mjx-c class="mjx-c75"></mjx-c><mjx-c class="mjx-c73"></mjx-c></mjx-mtext></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mtext>Radius</mtext></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="76" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c38"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>8</mn></math></mjx-assistive-mml></mjx-container></span> at 1:22</p></li>
      <li data-marker="*"><p class="sd-card-text"><span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="77" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c50"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>PT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="78" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c31"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c30"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1.0</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="79" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>RT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="80" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c32"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>2.2</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="81" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c61"></mjx-c><mjx-c class="mjx-c64"></mjx-c><mjx-c class="mjx-c69"></mjx-c><mjx-c class="mjx-c75"></mjx-c><mjx-c class="mjx-c73"></mjx-c></mjx-mtext></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mtext>Radius</mtext></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="82" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c37"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>7</mn></math></mjx-assistive-mml></mjx-container></span> at 2:26</p></li>
      <li data-marker="*"><p class="sd-card-text"><span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="83" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c50"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>PT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="84" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c31"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1.2</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="85" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>RT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="86" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c32"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c35"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>2.5</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="87" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c61"></mjx-c><mjx-c class="mjx-c64"></mjx-c><mjx-c class="mjx-c69"></mjx-c><mjx-c class="mjx-c75"></mjx-c><mjx-c class="mjx-c73"></mjx-c></mjx-mtext></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mtext>Radius</mtext></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="88" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c36"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>6</mn></math></mjx-assistive-mml></mjx-container></span> at 3:14</p></li>
      <li data-marker="*"><p class="sd-card-text"><span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="89" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c50"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>PT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="90" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c31"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c35"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>1.5</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="91" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-msub><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c54"></mjx-c></mjx-mtext><mjx-script style="vertical-align: -0.15em;"><mjx-texatom size="s" texclass="ORD"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c53"></mjx-c><mjx-c class="mjx-c70"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c65"></mjx-c><mjx-c class="mjx-c64"></mjx-c></mjx-mtext></mjx-texatom></mjx-script></mjx-msub></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><msub><mtext>RT</mtext><mrow data-mjx-texclass="ORD"><mtext>Speed</mtext></mrow></msub></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="92" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c33"></mjx-c><mjx-c class="mjx-c2E"></mjx-c><mjx-c class="mjx-c32"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>3.2</mn></math></mjx-assistive-mml></mjx-container></span>, <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="93" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mtext class="mjx-n"><mjx-c class="mjx-c52"></mjx-c><mjx-c class="mjx-c61"></mjx-c><mjx-c class="mjx-c64"></mjx-c><mjx-c class="mjx-c69"></mjx-c><mjx-c class="mjx-c75"></mjx-c><mjx-c class="mjx-c73"></mjx-c></mjx-mtext></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mtext>Radius</mtext></math></mjx-assistive-mml></mjx-container></span> = <span class="math notranslate nohighlight"><mjx-container class="MathJax CtxtMenu_Attached_0" jax="CHTML" tabindex="0" ctxtmenu_counter="94" style="font-size: 113.1%; position: relative;"><mjx-math class="MJX-TEX" aria-hidden="true"><mjx-mn class="mjx-n"><mjx-c class="mjx-c35"></mjx-c></mjx-mn></mjx-math><mjx-assistive-mml unselectable="on" display="inline"><math xmlns="http://www.w3.org/1998/Math/MathML"><mn>5</mn></math></mjx-assistive-mml></mjx-container></span> at 4:32</p></li>
    </ul>
  </li>
</ul></div>
</details></section>
<section id="noisy-chase">
<h3>Noisy Chase<a class="headerlink" href="#noisy-chase" title="Permalink to this heading">#</a></h3>
<p>Since the positions are noisy, I was thinking of using Kalman Filter to estimate the state of turtle from noisy measurements. I attempted to handle noisy <code class="docutils literal notranslate"><span class="pre">/rt_noisy_pose</span></code> using a Kalman Filter to estimate RT’s true state while keeping the rest of my approach same as mentioned above. I have tried the implementation, but the results were inconsistent, leading to cases where PT failed to catch RT. Implementation can be found in <a class="reference external" href="https://github.com/ABD-01/fluffy-fiesta/blob/master/scripts/turtle_noisy_chase.py"><code class="docutils literal notranslate"><span class="pre">turtle_noisy_chase.py</span></code></a>.</p>
<p>Apart from the Kalman Filter, I thought of an alternative approach to improve robustness against noisy data. Since Goal 5 involved deducing RT’s circular trajectory (center and radius) using the Kåsa circle fitting algorithm, we can project the noisy <code class="docutils literal notranslate"><span class="pre">/rt_noisy_pose</span></code> points onto the deduced circle to refine RT’s estimated position. <br />
The logic:</p>
<ol class="arabic simple">
<li><p>Use the fitted circle’s center <code class="docutils literal notranslate"><span class="pre">(a,</span> <span class="pre">b)</span></code> and radius <code class="docutils literal notranslate"><span class="pre">r</span></code> from Goal 5.</p></li>
<li><p>For each noisy pose <code class="docutils literal notranslate"><span class="pre">(x_n,</span> <span class="pre">y_n)</span></code>, find a point <code class="docutils literal notranslate"><span class="pre">(x_p,</span> <span class="pre">y_p)</span></code> on the circle that is closest to <code class="docutils literal notranslate"><span class="pre">(x_n,</span> <span class="pre">y_n)</span></code>.</p></li>
<li><p>Use the projected point <code class="docutils literal notranslate"><span class="pre">(x_p,</span> <span class="pre">y_p)</span></code> as RT’s estimated position for distance checks and predictions.</p></li>
</ol>
<p>The reason I think this could work is because, RT is guaranteed to move on the deduced circle (as validated in Goal 5), projecting noisy points onto this circle provides a better heuristic for RT’s true position. This should reduce the impact of noise (e.g., outliers) and improve the accuracy of the distance check for catching RT.</p>
</section>
</section>
<section id="conclusion">
<h2>Conclusion<a class="headerlink" href="#conclusion" title="Permalink to this heading">#</a></h2>
<p>This assignment has been a rewarding journey into robotics, motion control, and state estimation, providing me a chance to refresh my skills in ROS, PID control, and trajectory prediction in the TurtleSim environment.</p>
<p>I am grateful to the FlytBase team for this.</p>
<p>All video demonstrations are uploaded to Google Drive and can be accessed here: <a class="reference external" href="https://drive.google.com/drive/folders/1ydLdfyyXk5Fcxr_5_wix2LNsLm-eY18f?usp=drive_link">Videos</a>. ROSbag files for visualization with PlotJuggler are also available for further analysis: <a class="reference external" href="https://drive.google.com/drive/folders/1iBVvZHUEcOhlKGnKNgUc6l_yehRgtIUG?usp=sharing">ROSbag Files</a>.</p>
<p>You can also veiw the <a class="reference external" href="https://github.com/ABD-01/fluffy-fiesta/blob/master/CHANGELOG.md">CHANGELOG</a> to see the progress of the project.
The code is available on GitHub: <a class="reference external" href="https://github.com/ABD-01/fluffy-fiesta">Code</a>.</p>
<section id="challenges-and-reflections">
<h3>Challenges and Reflections<a class="headerlink" href="#challenges-and-reflections" title="Permalink to this heading">#</a></h3>
<p>Prior to this, I had not used PlotJuggler for visualization, but now I guess I am never going back to rqt.</p>
<p>Additionally, time constraints limited my ability to fully complete the noisy chase implementation (Goal 6). With more time, I am confident I could have integrated the circle projection method to achieve better results.</p>
<p>Thank you for reviewing my work and considering my submission for the Robotics Engineer role at FlytBase.</p>
</section>
</section>
<section id="references">
<h2>References<a class="headerlink" href="#references" title="Permalink to this heading">#</a></h2>
<ul class="simple">
<li><p><a class="reference external" href="https://youtu.be/9kFRecDU1bg">PlotJuggler: The Best Time Series Visualization Tool for ROS</a></p></li>
<li><p><a class="reference external" href="https://youtu.be/dMRDzicSvXk">PID controller Simple explanation with a Quadcopter as example</a></p></li>
<li><p><a class="reference external" href="https://youtu.be/DAwnXoQU-uk">Control design for a unicycle - feedback linearisation, with Matlab and ROS simulation</a></p></li>
<li><p><a class="reference external" href="https://nu-msr.github.io/navigation_site/lectures/circle_fit.html">Lecture 18: Circle Fitting - ME495 Sensing, Navigation, and Machine Learning for Robotics</a></p></li>
<li><p><a class="reference external" href="https://projecteuclid.org/journals/electronic-journal-of-statistics/volume-3/issue-none/Error-analysis-for-circle-fitting-algorithms/10.1214/09-EJS419.full">A. Al-Sharadqah and N. Chernov, Error Analysis for Circle Fitting Algorithms, Electronic Journal of Statistics (2009), Volume 3 p 886-911</a></p></li>
<li><p><a class="reference external" href="https://scipy.github.io/old-wiki/pages/Cookbook/Least_Squares_Circle.html">Cookbook/Least_Squares_Circle - SciPy</a></p></li>
<li><p><a class="reference external" href="https://github.com/ABD-01/ros_pid">Learning basics of ROS and PID controller-ABD</a></p></li>
<li><p><a class="reference external" href="https://youtu.be/IFeCIbljreY">Visually Explained: Kalman Filters</a></p></li>
<li><p><a class="reference external" href="https://motion.cs.illinois.edu/RoboticSystems/WhatIsMotionPlanning.html">Chapter 8. What is motion planning?</a></p></li>
<li><p><a class="reference internal" href="../ra/"><span class="doc std std-doc">Racecar Visual Line Follow - RoboticsAcademy</span></a></p></li>
</ul>
</section>
<section id="feedback">
<h2>Feedback<a class="headerlink" href="#feedback" title="Permalink to this heading">#</a></h2>
<p>You can share your feedback here.</p>
<div class="sd-container-fluid sd-sphinx-override sd-mb-4 docutils">
<div class="sd-row sd-row-cols-1 sd-row-cols-xs-1 sd-row-cols-sm-1 sd-row-cols-md-1 sd-row-cols-lg-2 docutils">
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
        <textarea name="message" rows="4" style="width: 90%;" placeholder="The best report I have ever seen"></textarea>
    </div>
    <button id="submitButton">Submit</button>
</form>

<script>
var submitMessage = document.getElementById("submitButton"),
    ContactForm = document.getElementById("ContactForm");

function submit(){
    const whToken = '5N6d1sN6AXGt-vMu1nFjMyc8xoSYM8iWAzPGFLU8z1pzsqsRiKrAyCI_Y2sIhVtkCZvY';
    const whId = "1347760695600742463";
    var url = `https://discord.com/api/webhooks/${whId}/${whToken}`;

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
      "content": "<@701479951479865384>, you have a new message from the flytbase_asgn!",
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
</div>
</div>
<!-- Links -->
</section>
</section>

       
