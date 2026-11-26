---
date:
  created: 2026-11-22
categories:
  - Engineering
slug: devops-notes-01-loop-and-testing
description: "First of a series of notes on DevOps: its eight-phase loop, CI/CD, culture and metrics, and where testing fits, from shift-left to shift-right."
cover: img/devops-cover.png
tags:
  - DevOps
  - Testing
  - CI/CD
  - Series
---

# DevOps notes, part 1: the loop, and testing on both sides of it

This post opens a second series of notes, this time on DevOps. It starts with what DevOps is and why it exists: the loop it is usually drawn as, the automation and culture behind it, and how teams measure it. Then it turns to a question that every fast-moving team runs into sooner or later: if we ship this often, where does the testing go? The answer has two directions, shift left and shift right, and a team needs both.

<!-- more -->

## Before DevOps

For a long time, building software and running it were two different jobs, done by two different teams. Developers wrote the code. Operations installed it on servers, kept it running and were woken up at night when it stopped. The two teams were measured on opposite things: developers on how much they changed, operations on how little broke. Every change was a risk to operations, so changes were collected and released together, a few times a year.

Large, rare releases are the worst of both worlds. Each one contains so many changes that when something fails nobody knows which change caused it. Developers have moved on to other work by the time the problems appear. Operations learns how the software behaves only after it is live, and the feedback reaches developers months late, if at all. When a release goes wrong, each side has a good reason to blame the other.

## What DevOps is

DevOps is the answer to that split. The name joins development and operations, and it appeared around 2009, when Patrick Debois organised the first DevOpsDays conference in Ghent. It is not a job title, a tool or a team, although it is often sold as all three. It is a combination of culture, practices and tools that makes one team responsible for its software from the first idea to its behaviour in production.

The central practice is to make changes small and frequent. A small change is easy to review, easy to test, and easy to undo if it fails. Many small releases also mean fast feedback: a developer learns how a change behaves in production days or hours after writing it, not months. The goal is not speed for its own sake. It is speed and stability together, and the surprising finding of the last fifteen years is that the two support each other.

## The loop

DevOps is usually drawn as a loop shaped like an infinity sign, with development on one side, operations on the other, and eight phases that never stop.

<figure markdown="span">
  {% include "devops-loop.svg" %}
  <figcaption>The DevOps loop. Development (blue) plans, codes, builds and tests; operations (vermilion) releases, deploys, operates and monitors, and what monitoring shows feeds the next plan. Testing runs around the whole loop, moving earlier with shift left and into production with shift right.</figcaption>
</figure>

- **Plan.** Decide what to build next, as small items in a backlog, from user requests, bug reports and what monitoring has shown.
- **Code.** Write the change in a branch under version control, usually Git, and have a colleague review it before it is merged.
- **Build.** Compile the code and package it, more and more often as a container image, on a continuous integration server.
- **Test.** Run the automated tests on every change, so a broken build is found within minutes.
- **Release.** Mark a build that passed as a versioned artefact, stored in a registry, ready to go to production.
- **Deploy.** Put the release into an environment, with the infrastructure itself described in code, for example on Kubernetes.
- **Operate.** Run the software: scale it with the load, apply patches, handle incidents.
- **Monitor.** Watch what it does, through metrics, logs, traces and alerts, and how users actually use it.

What monitoring reveals becomes input for planning, and the loop starts again. There is no last phase, which is why the loop is drawn as infinity and not as a line.

## CI/CD and automation

A loop that turns many times a week only works if most of it runs without people. That is the job of CI/CD.

**Continuous integration** means that everyone merges their work into the main branch often, at least daily, and every merge is built and tested automatically. Problems show up when they are small and fresh, not in a painful integration week before a release.

**Continuous delivery** goes one step further: every change that passes the pipeline is ready to be released, and releasing is a decision, often a single button. **Continuous deployment** removes the button. Every change that passes all checks goes to production on its own.

Two habits make this possible. The pipeline is written as code, in a file next to the application, so it is versioned and reviewed like everything else. The infrastructure is also written as code, with tools such as Terraform or Ansible, so an environment can be rebuilt exactly instead of being configured by hand and slowly drifting. Automation is what makes small batches affordable: if each release takes a day of manual work, nobody releases twenty times a week.

## Culture: CALMS

Tools are the visible part of DevOps and the easiest to buy, which is why it is so often mistaken for them. The acronym CALMS is a reminder of the rest. John Willis and Damon Edwards proposed CAMS, and Jez Humble later added the L.

- **Culture.** One team owns the result. Werner Vogels of Amazon put it as "you build it, you run it": the people who write a service are also on call for it.
- **Automation.** Repetitive work is done by machines, so people are free for the work that needs judgement.
- **Lean.** Work flows in small batches, and waiting and hand-offs are treated as waste.
- **Measurement.** Decisions rest on data about the system and the process, not on opinion.
- **Sharing.** Knowledge, tools and lessons move freely between teams.

The habit that best shows this culture is the blameless postmortem. After an incident the team writes down what happened and why the system allowed it, and does not ask who to punish. People who are not afraid of blame report problems early and describe them honestly, and that is the only way the system improves.

## DevSecOps

Security used to be a gate at the end: a review or a penetration test just before release, which either delayed the release or was skipped. DevSecOps moves security into every phase of the loop, as automated checks in the same pipeline:

- the dependencies and container images are scanned for known vulnerabilities on every build;
- static analysis looks for unsafe patterns in the code;
- secret detection stops passwords and keys from being committed;
- policy as code checks that the infrastructure follows the rules, such as no public storage and encryption everywhere, before it is created.

Security becomes part of everyone's daily work instead of one team's final verdict. The same idea, applied to testing, is shift left, which we come to below.

## Measuring delivery: the DORA metrics

How do you know whether DevOps is working? The research programme DORA (DevOps Research and Assessment), led by Nicole Forsgren, Jez Humble and Gene Kim, surveyed thousands of teams and found four measures that separate strong performers from weak ones:

- **Deployment frequency.** How often the team releases to production.
- **Lead time for changes.** How long a change takes from commit to running in production.
- **Change failure rate.** What fraction of releases cause a failure in production.
- **Time to restore service.** How long it takes to recover when one does.

The first two measure speed and the last two stability, and the research found that the best teams are good at all four at once. Speed and stability are not a trade-off. Teams that release in small, frequent batches also fail less often and recover faster.

## Velocity needs quality

Speed without quality is worth little. Releasing twenty times a week only helps if the releases work. In the old model, quality was a phase: a test team received a finished build and tested it for weeks. In a loop that turns every day there is no room for such a phase, and there should not be one.

Testing has to run around the whole loop instead, which is called continuous testing. It moves in two directions from where it used to sit. It moves left, to earlier in the loop, so that problems are found when they are cheap to fix. And it moves right, into production, so that problems no one could predict are found safely.

## Shift left: testing the expected, earlier

On a timeline drawn from left to right, design and code are on the left and production on the right. To shift left is to move testing towards the start. The reason is cost: a defect found while the code is being written takes minutes to fix. The same defect found in production may take days, plus an incident, plus the trust of users.

Shift left is a layered set of automated checks that run on every change:

- **Unit tests** check single functions and classes, in milliseconds.
- **Component tests** check one module or service on its own.
- **API and contract tests** check that services keep the agreements other services rely on.
- **Integration tests** check services together. Where a dependency is not ready or too costly to call, a mock or a virtual service stands in for it, so integration can be tested long before everything exists.
- **Static analysis** finds bugs, style problems and security issues without running the code at all.

The tests are written in the same sprint as the code they test, not afterwards. Each new feature then adds its tests to the regression suite, and the suite grows with the product.

All this depends on a good test automation framework, and four properties matter most:

- **It works with the team's tools.** It runs tests written with the tools the team already uses instead of forcing one on everyone, while still giving one standard structure and one combined report.
- **It survives changes to the application.** It tests through the API layer where possible, because interfaces change less often than screens, and it is designed so that one change in the application means one change in the tests, not fifty.
- **It runs everywhere.** The same tests run in the cloud and on premises, in different browsers and on mobile, with little more than a change of configuration.
- **It is fast.** A suite that takes hours will be skipped. Feedback has to arrive while the developer still remembers the change.

Shift left has a limit, and it is built in. It tests what someone expected. Every test is a question someone thought to ask, and the most expensive failures tend to come from questions no one thought of.

## Shift right: exploring the unknown, in production

Modern systems are too complex to predict completely: dozens of services, real users doing things no one designed for, real data, real load and real failures of networks and machines. Some behaviour can only be seen in production. Shift right accepts this and tests there, carefully, with the risk kept small.

Shift right does not mean releasing untested code and waiting for complaints. It is a set of techniques that expose a change to reality in a controlled way:

- **Beta and canary releases.** A new version first goes to a small group, such as employees, volunteers or 1% of traffic, while monitoring compares it with the old version. If the canary falters, few users notice and the release is rolled back. The name comes from the canaries miners carried to warn them of gas.
- **Feature toggles.** New code ships switched off and is turned on by configuration, without a new deployment. An experiment toggle sends some users down a new code path and others down the old one, so the two can be compared. An ops toggle lets operators switch a new feature off at once if it hurts performance. Toggles are powerful, but every one is a branch in the code that someone must eventually remove.
- **Traffic shadowing.** Before a new version of a service replaces the old one, a copy of the real production requests is also sent to the new version, running on the side. Users only ever see the old version's answers. The new version's answers are compared with them, and any difference is a question worth asking. It tests against real production traffic without risk to users and without building a huge set of test data.
- **A/B testing.** Two working versions of a page or feature run side by side, each for part of the users, to see which one leads to the behaviour you want, such as more completed purchases. It tests the product decision rather than the correctness of the code.
- **Chaos engineering.** If failures in production cannot be avoided completely, cause small ones on purpose and watch what happens. Netflix built Chaos Monkey to shut down random servers in production, so that its engineers had to build services that survive it. A controlled experiment in daylight is far better than the same failure, unplanned, at three in the morning.

All of these depend on the right end of the loop being strong. Without good monitoring a canary teaches nothing, and without fast rollback an experiment can become an outage. Shift right also has its own cost. A problem found in production is found late, and the fix has to go through the whole loop again.

## Both, not either

Shift left and shift right are not competitors. They answer different questions.

| | Shift left | Shift right |
|---|---|---|
| When | before a change is merged or released | after release, with real users and real traffic |
| Question | does it do what we expect? | what does it do that we did not expect? |
| Techniques | unit, component, API, contract and integration tests, static analysis | canary and beta releases, feature toggles, traffic shadowing, A/B tests, chaos engineering |
| Catches | logic errors, broken interfaces, regressions | behaviour under real load, data and usage; weak points in resilience |
| Cost | cheap to fix; only finds what someone thought to test | finds the unknown; fixes come late and need care to stay safe |

A team that only shifts left releases code that passes every test and still surprises it in production. A team that only shifts right uses its users as its test suite. How much of each a team needs depends on its system, its risks and its users: a bank and a photo-sharing app will strike different balances. Both are part of continuous testing, and together they cover the whole loop.

## What comes next

This is the first part of a series of DevOps notes, written as I go. Later parts will go deeper into single topics: a CI/CD pipeline built step by step, containers and Kubernetes, infrastructure as code, and observability. The code and examples will go into a GitHub repository, which I will link here when the first hands-on part arrives.

If you work on these problems, I would like to hear how your team balances shift left and shift right. Write to me by [email](mailto:saeed.taghavi.v@gmail.com) or on [LinkedIn](https://www.linkedin.com/in/saeed-taghavi-a16488130/).
