from collections import namedtuple
from enum import Enum

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))


def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    participants = [
        agent for agent in agent_listing
        if agent.category in {Condition.CURE, Condition.SICK, Condition.DYING}
    ]
    non_participants = [
        agent for agent in agent_listing
        if agent.category in {Condition.HEALTHY, Condition.DEAD}
    ]

    updated_participants = []

    for i in range(0, len(participants), 2):
        if i + 1 >= len(participants):
            updated_participants.append(participants[i])
        else:
            a = participants[i]
            b = participants[i + 1]

            if a.category == Condition.CURE or b.category == Condition.CURE:
                new_a = a if a.category == Condition.CURE else Agent(a.name, improve(a.category))
                new_b = b if b.category == Condition.CURE else Agent(b.name, improve(b.category))
            else:
                new_a = Agent(a.name, worsen(a.category))
                new_b = Agent(b.name, worsen(b.category))
            updated_participants.extend([new_a, new_b])

    return updated_participants + non_participants


def improve(category):
    if category == Condition.SICK:
        return Condition.HEALTHY
    elif category == Condition.DYING:
        return Condition.SICK
    return category


def worsen(category):
    if category == Condition.SICK:
        return Condition.DYING
    elif category == Condition.DYING:
        return Condition.DEAD
    return category
