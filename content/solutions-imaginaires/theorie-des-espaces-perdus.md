---
title: "The Sidenote Stress Test"
date: 2023-10-27
summary: "An engineering calibration document to verify the dual-stack physics engine of the marginalia system."
tags: ["Architecture", "System Check"]
featured_image: "" 
---

This document exists to test the **Alternating Collision Logic**. We need to ensure that notes stacked on the left do not interfere with notes stacked on the right, and that vertical collisions are resolved independently.

### The First Cluster (Left vs Right)

Here is a standard paragraph initiating the sequence. We place a note here {{< sidenote >}}**Note 1 (Left)**: This should appear on the Left. It is the first note (Odd). It has enough text to establish a baseline height.{{< /sidenote >}} to start the Left Stack.

Immediately following, we have a second sentence with a note {{< sidenote >}}**Note 2 (Right)**: This should appear on the Right. It is the second note (Even). It should align roughly with the line it was called from, without caring about Note 1's position.{{< /sidenote >}}.

### The Collision Cluster (Vertical Stress)

Now we attempt to break the layout. This paragraph has three notes in rapid succession.

1. First, we trigger an odd note {{< sidenote >}}**Note 3 (Left)**: This is a Left note. It is very close to Note 1 vertically. If the logic works, it might push down slightly if Note 1 is long, but it should NOT care about Note 2 on the right.{{< /sidenote >}}.
2. Second, we trigger an even note {{< sidenote >}}**Note 4 (Right)**: This is a Right note. It is physically below Note 2. Let's make this one **very long** to force a collision with any subsequent right-side notes. It contains filler text to expand its height significantly. Lorem ipsum dolor sit amet, consectetur adipiscing elit.{{< /sidenote >}}.
3. Third, another odd note {{< sidenote >}}**Note 5 (Left)**: Back to the left. This note is geographically close to Note 4 in the source text, but physically, it lives on the left wall. It should not be pushed down by the massive Note 4 on the right.{{< /sidenote >}}.

### The Footer Check

Finally, we ensure the container extends. Here is a final note {{< sidenote >}}**Note 6 (Right)**: This note pushes the boundaries. It forces the article container to calculate the 'Lowest Point' between the Left and Right stacks and extend the padding-bottom accordingly so we don't bleed into the footer ornament.{{< /sidenote >}} at the very end of the document.