---
draft: true
date:
  created: 2026-11-23
categories:
  - Engineering
slug: devops-notes-02-voting-app-roadmap
description: "Part 2 of the DevOps notes: one five-part app on one machine with no cloud, and the plan from Docker Compose and kind to GitLab CI and chaos engineering."
cover: img/devops-voting-cover.png
tags:
  - DevOps
  - Docker
  - Kubernetes
  - Series
---

# DevOps notes, part 2: one app, one machine, and the road ahead

[Part 1](devops-notes-01-loop-and-testing.md) was the map: the DevOps loop, the culture around it, and where testing fits. From here on the notes get practical. Each post takes one topic, such as containers, Kubernetes, a pipeline, monitoring or an A/B test, and applies it to the same small application on the same machine. This post introduces the application, the lab it runs in, and the plan.

<!-- more -->

## The app

The series is built on the [example voting app](https://github.com/dockersamples/example-voting-app) published by Docker under the Apache 2.0 licence, which has become a standard teaching example. It does one thing. Visitors vote for one of two options, cats or dogs by default, and anyone can watch the totals change live.

Behind that one thing are five parts:

- **vote** is a small web page written in Python. It shows the two options and accepts a vote.
- **redis** is an in-memory store used as a queue. The vote page pushes every vote onto it and returns at once, without waiting for anything else.
- **worker** is a background program written in .NET. It takes votes off the queue one by one and stores them.
- **postgres** is the database. It keeps one row per voter, so a voter who changes their mind replaces their vote instead of adding a second one.
- **result** is a second web page, written in Node.js. It reads the totals from the database and pushes them to the browser as they change.

<figure markdown="span">
  {% include "voting-app.svg" %}
  <figcaption>The path of a vote. The vote page pushes it to a Redis queue, the worker takes it from the queue and stores it in Postgres, and the result page reads the totals. Services are in blue, data stores in amber.</figcaption>
</figure>

## Why this app

A to-do list would be simpler. This app is better for learning DevOps, because it is small but has the shape of real systems:

- **Three languages.** Python, .NET and Node.js each need their own build, their own base image and their own test tools, just as in a real company where teams choose different stacks.
- **Two web front ends and a background worker.** Some parts face users and must answer quickly; one part works in the background and only has to keep up.
- **A queue and a database.** The vote, worker and result services hold no state and can be restarted or copied freely. Redis and Postgres hold data, and losing them means losing votes. Stateless and stateful parts need very different care, and both are here.
- **Parts that fail independently.** If the worker stops, votes pile up in the queue and nothing is lost until the queue itself fails. If the database stops, the result page has nothing to show but voting still works. These are exactly the situations that monitoring, alerts and chaos experiments are about.

Every topic in DevOps has something to act on in this app, and it stays small enough to understand completely.

## The lab: everything on one machine

The whole series runs on a single computer, with no cloud account and no bill. Once the container images have been downloaded, it works offline.

- **Linux and Docker.** Any Linux machine works, and so does Windows with WSL 2. Docker runs every service in a container.
- **kind** ("Kubernetes in Docker") creates a complete Kubernetes cluster out of containers in a few seconds, and deletes it as fast. One laptop can hold several clusters, for example one for development and one for production.
- **A local GitLab.** GitLab runs in Docker too, with its own container registry and a runner that executes pipelines. The pipelines in this series are GitLab CI pipelines running on the same machine as everything else.

There are good reasons to stay local beyond the cost. Every component is visible: nothing is hidden behind a managed service whose inside you cannot see. Mistakes are cheap, since a broken cluster is deleted and recreated in a minute. And anyone can rebuild the lab from the notes, which is the point of writing them.

## The road ahead

This is the plan as it stands. It will change as the series goes on: some topics will need two posts, and others will turn out to belong together.

| Part | Topic | Tools |
|---|---|---|
| | **Containers** | |
| 3 | Run the app with Docker Compose: networks, volumes, health checks, start-up order | Docker Compose |
| 4 | Dockerize each service well: multi-stage builds, small images, non-root users, tags | Dockerfile |
| 5 | A local container registry | Docker Registry |
| | **Testing, shifted left** | |
| 6 | Unit tests for each service, in its own language | pytest, Jest, xUnit |
| 7 | Integration and end-to-end tests against a running stack | Compose, Testcontainers |
| | **Kubernetes** | |
| 8 | A local cluster | kind, kubectl |
| 9 | Deployments, Services and Ingress for the app | Kubernetes, ingress-nginx |
| 10 | Configuration and secrets, with overlays for dev and prod | ConfigMaps, Secrets, Kustomize |
| 11 | Databases on Kubernetes: StatefulSets, volumes, backup and restore | Postgres, Redis |
| 12 | Packaging the app as a chart | Helm |
| | **Automation** | |
| 13 | Prepare a machine and deploy the stack with playbooks | Ansible |
| 14 | The cluster and its add-ons as code | Terraform |
| | **CI/CD** | |
| 15 | A local GitLab with a registry and a runner | GitLab, GitLab Runner |
| 16 | The pipeline: lint, test, build, scan, push | GitLab CI, Trivy |
| 17 | Deploying from the pipeline, and GitOps | GitLab CI, Argo CD |
| | **Observability** | |
| 18 | Metrics from the app and the cluster | Prometheus |
| 19 | Dashboards and alerts | Grafana, Alertmanager |
| 20 | Logs in one place | Loki |
| | **Shift right and reliability** | |
| 21 | Load tests and autoscaling | k6, HorizontalPodAutoscaler |
| 22 | Canary releases and feature flags | Argo Rollouts |
| 23 | Designing an A/B test on the vote page: hypothesis, traffic split, sample size, decision | Kubernetes, Python |
| 24 | Breaking things on purpose | Chaos Mesh |
| 25 | Security: image scanning, SBOMs, network policies, secrets | Trivy, Syft, Vault |
| 26 | Backup and disaster recovery for the whole lab | Velero, pg_dump |

The order follows the loop from part 1. The app first has to run and be packaged (containers). It has to be checked before anything else is built on it (testing). Then it moves to a real orchestrator (Kubernetes) and its setup is automated (Ansible, Terraform). After that, everything is tied into a pipeline (CI/CD). The last two stages are about watching the running system and learning from it in production (observability, shift right). The A/B test in part 23 is the one I look forward to most. Designing a good experiment is mostly statistics, not tooling, and it is where the right end of the loop meets the scientific method.

## How the code will be organised

All the code will live in one repository, with one folder per post: `03-compose/`, `04-dockerfiles/` and so on. Each folder is self-contained, with its own README, the files for that step and the commands to run it, so a reader can jump in at any post without replaying the ones before. Where a post changes the application itself, the folder carries the changed copy. I will add the link here when part 3 brings the first code.

## What comes next

Part 3 starts the lab: running the five services together with Docker Compose, and looking at what Compose does for us, from the network that lets the services find each other to the volume that keeps the votes when the database restarts.

If you have built a similar lab, or there is a topic you would like to see in the list, write to me by [email](mailto:saeed.taghavi.v@gmail.com) or on [LinkedIn](https://www.linkedin.com/in/saeed-taghavi-a16488130/).
