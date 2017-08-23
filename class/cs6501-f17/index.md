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

The reviews must be emailed to bradjc@virginia.edu before the start of each class
and should be used as reference notes for the in-class discussion.

Note: it will always be easier to find weaknesses that it is to find strengths
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
3. Monday, November 27: Five to size page paper with preliminary results.
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


| Class      | Topic                             | Lead | Details                                                                                                 |
|------------|-----------------------------------|------|---------------------------------------------------------------------------------------------------------|
| Wed Aug 23 | [Introduction](slides/01-introduction.pptx) |      |                                                                                                         |
| Mon Aug 28 | Ubiquitous computing and the IoT  |      | No reviews: (1) [Ubiquitous Computing](weiser93ubiquitous.pdf), (2) [IoT Research Challenges](iot_challenges.pdf) |
|            | **Applications**                  |      |                                                                                                         |
| Wed Aug 30 | Outdoor and Wildlife Monitoring   |      | (1) [Great Duck Island](szewczyk04greatduckisland.pdf), (2) [Bat Tracking](sommer16battracking.pdf)             |
| Mon Sep 4  | Urban Environments                |      | (1) [Array of Things](catlett17aot.pdf), (2) [Air Quality](devarakonda13airquality.pdf)                         |
| Wed Sep 6  | Buildings and Energy              |      | (1) [Sentinel](balaji13sentinel.pdf), (2) [CapNet](saifullah14capnet.pdf)                                       |
| Mon Sep 11 | Democratic Monitoring             |      | (1) [SeaGlass](ney17seaglass.pdf)                                                                           |
| Wed Sep 13 | Personal and Population Health    |      | (1) [LIBS](nguyen16libs.pdf), (2) [Opo](huang14opo.pdf)                                                         |
| Mon Sep 18 | Infrastructure and Industrial     |      | (1) [Pipeline](nachman07pipeline.pdf), (2) [Alps](lazik15alps.pdf)                                              |
| Wed Sep 20 | Safety and Security               |      | (1) [Gunshot Detection](sallai11gunshot.pdf), (2) [LOOKUP](jain15lookup.pdf)                                    |
| Mon Sep 25 | Project Workshop 1                |      | Bring first version to class.  |
|            | **Sensors, Hardware, Energy**     |      |                                                                                                         |
| Wed Sep 27 | Hardware Platforms and Smart Dust |      | (1) [TelosB](polastre05telos.pdf), (2) [Firestorm](anderson16firestorm.pdf), (3) [M3](??)                           |
| Mon Oct 2  | Energy Harvesting 1               |      | (1) [HydroWatch](taneja08hydrowatch.pdf), (2) [Monjolo](debruin13monjolo.pdf)                                   |
| Wed Oct 4  |                                   |      | No class (Reading day)                                                                                  |
| Mon Oct 9  | Energy Harvesting 2               |      | (1) [DoubleDip](martin12doubledip.pdf), (2) [Tragedy of the Coulombs](hester15tragedyofthecoulombs.pdf)         |
| Wed Oct 11 | Hardware Generation and Sensing 1 |      | (1) [EDG](ramesh17edg.pdf), (2) [Soli](lien16soli.pdf)                                                           |
| Mon Oct 16 | Sensing 2                         |      | (1) [PASEM](lorek14pasem.pdf), (2) [Synthetic Sensors](laput17syntheticsensors.pdf)                             |
|            | **Networking and Interfacing**    |      |                                                                                                         |
| Wed Oct 18 | Low Power Wireless                |      | (1) [LPL](polastre04lpl.pdf), (2) [LWB](ferrari12lwb.pdf)                                                       |
| Mon Oct 23 | Multi- and Single-hop Networking  |      | (1) [IP is Dead, Long Live IP](hui08ip.pdf), (2) [Blend](julien17blend.pdf), LoRa                             |
| Wed Oct 25 | Project Workshop 2                |      | Bring second version of the project paper to class.                                                             |
| Mon Oct 30 | Backscatter and Whitespaces       |      | (1) [Interscatter](iyer16interscatter.pdf), (2) [SNOW](saifullah16snow.pdf)                                     |
| Wed Nov 1  | Gateways                          |      | (1) [Gateway Problem](zachariah15gateway.pdf), (2) [Fabryq](mcgrath15fabryq.pdf)                                |
| Mon Nov 6  |                                   |      | No class (SenSys). Work on project paper.                                                                         |
| Wed Nov 8  |                                   |      | No class (SenSys). Work on project paper.                                                                         |
|            | **Programming and Security**      |      |                                                                                                         |
| Mon Nov 13 | Operating Systems                 |      | (1) [SOS](han05dynamic.pdf), (2) [DINO](lucia15dino.pdf)                                                        |
| Wed Nov 15 | IoT Frameworks                    |      | (1) [Ravel](riliskis15ravel.pdf), (2) [HomeOS](dixon12homeos.pdf)                                               |
| Mon Nov 20 | IoT Security                      |      | (1) [SmartAuth](tian17smartauth.pdf), (2) [Electromyography](yang16electromyography.pdf)                        |
| Wed Nov 22 |                                   |      | No class (Thanksgiving)                                                                                 |
| Mon Nov 27 | Misusing Sensors                  |      | (1) [Gyrophone](michalevsky14gyrophone.pdf), (2) [PitchIn](han17pitchin.pdf). Final papers due.              |
|            | **End**                           |      |                                                                                                         |
| Wed Nov 29 | Project Presentations 1           |      |                                                                                                         |
| Mon Dec 4  | Project Presentations 2           |      |                                                                                                         |


