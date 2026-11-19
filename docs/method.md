# AutoMaster and Skill-FT

**Skill-FT is the training-data intervention.** A skill specifies a useful execution behavior: when it applies, what action changes, and how to judge the result. Selected skill instructions are appended to the Teacher's system prompt before rollout. The Teacher then interacts with tools and the environment to produce a new demonstration.

Skills can suppress an undesirable habit or elicit an effective behavior that appears too rarely. This includes improving already-successful executions: independently checking a numerical claim, verifying the final saved artifact, following retrieved evidence instead of a familiar guess, or testing an actual dependency interface.

**AutoMaster is the autonomous research system.** Its research agent examines Student trajectories, unguided Teacher trajectories and available reference-model trajectories. It designs interventions, tests them through pilot executions, revises their scope, expands useful candidates and selects demonstrations. Student SFT and evaluation provide feedback for further research. The research agent and the trained Student are separate roles.

## Behavioral shaping in practice

<table>
<tr>
<td width="33%" valign="top">
<h4>Verifying convergence</h4>
<a href="../assets/skills/figure5a.png"><img src="../assets/skills/figure5a.png" alt="Both solvers meet the error threshold. The unguided Teacher claims fourth-order accuracy; the guided Teacher diagnoses the numerical error and verifies convergence across grid resolutions." width="100%"></a>
<p>Both solvers meet the error threshold. The unguided Teacher claims fourth-order accuracy; the guided Teacher diagnoses the numerical error and verifies convergence across grid resolutions.</p>
<a href="../skills/tb2.1/execute-numeric-decision/SKILL.md">execute-numeric-decision</a>
</td>
<td width="33%" valign="top">
<h4>Finding the director</h4>
<a href="../assets/skills/figure5b.png"><img src="../assets/skills/figure5b.png" alt="Both searches identify the same episode. The unguided Teacher repeatedly guesses an award; the guided Teacher follows episode credits to identify the director, then checks the award clue." width="100%"></a>
<p>Both searches identify the same episode. The unguided Teacher repeatedly guesses an award; the guided Teacher follows episode credits to identify the director, then checks the award clue.</p>
<a href="../skills/bc/recover-search-anchor/SKILL.md">recover-search-anchor</a>
</td>
<td width="33%" valign="top">
<h4>Checking the sort order</h4>
<a href="../assets/skills/figure5c.png"><img src="../assets/skills/figure5c.png" alt="A flawed self-test prompts the unguided Teacher to reverse the sorting rule. The guided Teacher diagnoses the test input, preserves the required order, and passes 38 of 38 tests." width="100%"></a>
<p>A flawed self-test prompts the unguided Teacher to reverse the sorting rule. The guided Teacher diagnoses the test input, preserves the required order, and passes 38 of 38 tests.</p>
<a href="https://aweai-team.github.io/AutoMaster/assets/paper.pdf?v=e0be391fbd#page=9">Trace failures to their source · Figure 5c</a>
</td>
</tr>
</table>

## Skills and data selection work together

A skill can apply to many tasks, a task can receive several skills, and different subsets can use different combinations. Task subsets can overlap. The research agent selects individual generated demonstrations rather than assuming that every rollout using a skill is equally useful.

Task outcomes and learning value are distinct. A successful trajectory can contain weak behavior. In repository construction, a partially correct implementation can still demonstrate useful construction or diagnosis. The research process considers actual behavior alongside task feedback and data quality.

## Training and deployment

The selected demonstrations are used for standard supervised fine-tuning. The retained system prompt includes the skills used to produce that demonstration; supervision applies to assistant outputs. Each outer-round candidate starts from the initial Student checkpoint and is evaluated to inform subsequent research. At evaluation, the generated skills are not added to the Student's prompt.

The first public release contains a selected skill collection and inference recipes. The autonomous research controller, Teacher-generation service and SFT orchestration are not included in this release.
