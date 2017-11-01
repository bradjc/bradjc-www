---
permalink: "/class/cs6501-f17/"
layout: single
title:  "IoT Sensors and Systems"
---

<style>
.masthead {
	display: none;
}
</style>


- **Course**: CS6501/ECE6501 (008) - Fall 2017
- **Instructor**: Brad Campbell
- **Time**: M/W 10:30am-11:45am
- **Location**: 340 Rice
- **Office Hours**: Tu 2pm-3:30pm, 512 Rice

--------------------------------------------------------------------------------

The Internet of Things promises to revolutionize how we interact with computers
by making embedded computation ubiquitous. New devices will be added to cities,
to homes, to factories, to ourselves (inside and out), to cars, and to many
other facets of life. The hope is that this influx of technology will help us
solve many pressing societal issues in areas such as energy, personal health,
the environment, and safety. The challenges lie in designing and scaling the
hardware platforms, networking protocols, and programming paradigms to enable
this new class of computing to be used productively.

This course will start by covering several key application areas and various
systems that address issues within those applications. With the application
drivers in place, we will explore the hardware platforms that support the
sensing, energy, and deployment requirements of the various application domains.
With methods to build the IoT devices and ensure they are low power, we move to
techniques for providing connectivity to individual and networks of devices. We
then will investigate systems for programming and providing security primitives
for the networks of devices, as well as how the IoT can expose new privacy
concerns.

As a graduate seminar, this course will focus on reading, analyzing, and
discussing research papers. The course will focus on very recent research (last
2-5 years), but will also include older, more foundational papers for certain
topics.


Deliverables
------------

This seminar requires three main deliverables from students.

### 1. Paper Reviews

Before each class you must read and write a short review of each
assigned paper. The review should answer the following questions:

- What is the problem this paper addresses, and why is it important?
- What is the hypothesis of this paper?
- What are two key assumptions that this paper makes?
- What are the two main strengths of this paper?
- What are the two main weaknesses of this paper?
- Which figure or experiment was most compelling in support of the hypothesis,
  and why?

Additionally, the review should include ratings for how you perceive the paper
in the following categories:

- Presentation (1-5):
- Interest (1-5):
- Impact (1-5):
- Overall (1-5):
- Confidence (1-5):

The reviews must be entered in the [review
site](http://cs6501-008-f17-hotcrp.cs.virginia.edu/) before the start of each
class and should be used as reference notes for the in-class discussion.

Note: it will always be easier to find weaknesses than it is to find strengths
when reviewing a paper. After all, the authors had a limited number of pages!
Try to find the merits that lead to the paper getting accepted while you read
each paper.


### 2. In-class Discussion Lead

You must select one class where you will be the discussion lead for the assigned
papers. You should come prepared to give an overview of the paper, and guide a
discussion about the strengths, weaknesses, and potential for impact of the
paper.


### 3. Semester Project

This class will feature a semester long project focused on idea creation, idea
motivation, and the scientific method. You will choose a topic, develop a
hypothesis within that topic, develop a research plan to explore and evaluate
that hypothesis, provide some motivating preliminary data, and communicate these
results in the form of a written paper.

Note: this does not require actually building the system. In fact, it requires
that you _do not_ build the system, but rather work on the science aspects
before undertaking the engineering.

The project will have four milestones:

1. Monday, September 25: Two page paper covering your hypothesis, motivation,
and expected results.
2. Wednesday, October 25: Four page paper with planned experiments.
3. Monday, November 27: Five to six page paper with preliminary results.
4. Wednesday, November 29 and Monday, December 4: Project presentations.


For the two in-class project workshops, you will be expected to evaluate and
provide feedback for your peers' papers.



Grading
-------

Your grade for the course will be based on: individual or group project (34%),
paper reviews and peer-review of final projects (33%), and in-class
participation and discussion lead (33%).


Schedule
--------


| Class      | Topic                                                         | Lead     | Details                                                                                                           |
|------------|---------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| Wed Aug 23 | [Introduction](slides/01-introduction.pptx)                   | Campbell |                                                                                                                   |
| Mon Aug 28 | [Ubiquitous computing and the IoT](slides/02-ubiquitous.pptx) | Campbell | No reviews: (1) [Ubiquitous Computing](weiser93ubiquitous.pdf), (2) [IoT Research Challenges](iot_challenges.pdf) |
|            | **Applications**                                              |          |                                                                                                                   |
| Wed Aug 30 | [Outdoor and Wildlife Monitoring](slides/03-outdoor.pptx)     | Campbell | (1) [Great Duck Island](szewczyk04greatduckisland.pdf), (2) [Bat Tracking](sommer16battracking.pdf)               |
| Mon Sep 4  | Urban Environments                                            | Campbell | (1) [Array of Things](catlett17aot.pdf), (2) [Air Quality](devarakonda13airquality.pdf)                           |
| Wed Sep 6  | Buildings and Energy                                          | Campbell | (1) [Sentinel](balaji13sentinel.pdf), (2) [CapNet](saifullah14capnet.pdf)                                         |
| Mon Sep 11 | [Democratic Monitoring](slides/06-seaglass.pptx)              | Campbell | (1) [SeaGlass](ney17seaglass.pdf)                                                                                 |
| Wed Sep 13 | Personal and Population Health                                | Campbell | (1) [LIBS](nguyen16libs.pdf), (2) [Opo](huang14opo.pdf)                                                           |
| Mon Sep 18 | [Infrastructure and Industrial](slides/08-infra.pptx)         | Campbell | (1) [Pipeline](nachman07pipeline.pdf), (2) [Alps](lazik15alps.pdf)                                                |
| Wed Sep 20 | Safety and Security                                           | Anderson | (1) [Gunshot Detection](sallai11gunshot.pdf), (2) [LOOKUP](jain15lookup.pdf)                                      |
| Mon Sep 25 | [Project Workshop 1](peer_review_1.pdf)                       |          | Bring first version to class.                                                                                     |
|            | **Sensors, Hardware, Energy**                                 |          |                                                                                                                   |
| Wed Sep 27 | Hardware Platforms and Smart Dust                             | Campbell | (1) [TelosB](polastre05telos.pdf), (2) [M3](lee13modular.pdf), No review: (3) [Firestorm](anderson16firestorm.pdf) |
| Mon Oct 2  |                                                               |          | No class (Reading day)                                     |
| Wed Oct 4  | Energy Harvesting 1                                           | Campbell | (1) [HydroWatch](taneja08hydrowatch.pdf), (2) [Monjolo](debruin13monjolo.pdf)                                      |
| Mon Oct 9  | Energy Harvesting 2                                           | Campbell | (1) [Tragedy of the Coulombs](hester15tragedyofthecoulombs.pdf), No review: (2) [DoubleDip](martin12doubledip.pdf) |
| Wed Oct 11 | Hardware Generation and Sensing 1                             | Campbell | (1) [EDG](ramesh17edg.pdf), (2) [Soli](lien16soli.pdf), No review: (3) [Synthetic Sensors](laput17syntheticsensors.pdf) |
|            | **Networking and Interfacing**                                |          |                                                                                                                   |
| Mon Oct 16 | Low Power Wireless                                            | Crump    | (1) [LPL](polastre04lpl.pdf), (2) [LWB](ferrari12lwb.pdf)                                                         |
| Wed Oct 18 | Networking                                                    |          | (1) [IP is Dead, Long Live IP](hui08ip.pdf), (2) [Interscatter](iyer16interscatter.pdf)                                 |
| Mon Oct 23 | Gateways and Whitespaces                                      | Campbell | (1) [Gateway Problem](zachariah15gateway.pdf), (2) [SNOW](saifullah16snow.pdf)                                |
| Wed Oct 25 | [Project Workshop 2](peer_review_2.pdf)                       |          | Bring second version of the project paper to class.                                                               |
| Mon Oct 30 |                                                               |          | No class (SOSP).                                       |
|            | **Programming and Security**                                  |          |                                                                                                                   |
| Wed Nov 1  | Operating Systems                                             | TockOS   | (1) [SOS](han05dynamic.pdf), (2) [DINO](lucia15dino.pdf)                                |
| Mon Nov 6  |                                                               |          | No class (SenSys). Work on project paper.                                                                         |
| Wed Nov 8  |                                                               |          | No class (SenSys). Work on project paper.                                                                         |
| Mon Nov 13 | Blockchain: Hype or Useful?                                   |          | TBD                                                          |
| Wed Nov 15 | IoT Frameworks                                                | Hamid    | (1) [Ravel](riliskis15ravel.pdf), (2) [HomeOS](dixon12homeos.pdf)                                                 |
| Mon Nov 20 | IoT Security                                                  | Ulkuatam | (1) [SmartAuth](tian17smartauth.pdf), (2) [Electromyography](yang16electromyography.pdf)                          |
| Wed Nov 22 |                                                               |          | No class (Thanksgiving)                                                                                           |
| Mon Nov 27 | Misusing Sensors                                              | Agrawal  | (1) [Gyrophone](michalevsky14gyrophone.pdf), (2) [PitchIn](han17pitchin.pdf). Final papers due.                   |
|            | **End**                                                       |          |                                                                                                                   |
| Wed Nov 29 | Project Presentations 1                                       |          |                                                                                                                   |
| Mon Dec 4  | Project Presentations 2                                       |          |                                                                                                                   |

Notes for the future!
---------------------

- Maybe replace LWB with Glossy (or do both). Flooding + network protocol is
a lot to cover.
- OS papers were good choices.
