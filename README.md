# CyclometricComplexityDistribution
Name: Prashant Aggarwal
<br> ID: 17317559

<br>REPOSITORY USED: https://github.com/Prashant00005/Distributed_File_Systems

<br>The task for this project involved computing cyclomatic complexity of a particulat repository. Commander is responsible for allocating commits to subjects. When subjects receive work they pull the repository.
Run the commander.py to start the commander node. 

# Findings
I have uploaded two screenshots (Graph.jpeg, Value.jpeg) containing the values that I got after running the commander and subjects, and graph of Commander Vs Subjects. It can be infered from the graph that the performance is achieved maximum when the number of subjects are 8. Initially when there was only one subject, the execution time was very high. As the work was divided amonsgt the subjects execution time reduced. This time reduces till number of subjects were 8 and after that started increasing.

# Dependency
Dependies should be installed with following commands: <br>apt-get install python3 and apt-get install python3-pip.
<ul>
<li>Flask (0.12.2)
  <li>Flask-RESTful (0.3.6)
    <li>requests (2.9.1)
      <li>radon (2.1.1)

</ul>
