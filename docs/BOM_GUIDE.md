# Seizo Nexus: DIY build and bill of materials

**Owner's plan:** make the parts yourself. Do not budget paid printing services or purchased finished modules. Outside parts or services are acceptable only when genuinely free; that availability has not yet been confirmed. This is the Nexus workstation budget, not the robot controller or PCB/HAT budget.

## What goes in BOM.csv

The CSV is a **draft purchasing list, not a complete assembly inventory or approved funding request**. It retains the existing six-column format. Blank quantity, price and link fields mean unknown, not zero. There is no verified total yet.

| Entry | How to fill it |
| --- | --- |
| PLA filament for self-printed parts | Match the printer's required filament diameter. Choose the spool size and seller, then enter the number of spools, actual price per spool and product link. Quantity must follow a slicer estimate and available stock, not a guessed one-spool allowance. |
| Shipping | Enter the actual checkout quote. Use zero only when shipping is confirmed free or no order is needed. |
| Sales tax | Enter the actual checkout amount only when it is not already included in item prices. Do not count it twice. |

**Current material choice: PLA for initial room-temperature prototype and fit checks.** This is not a verified choice for every loaded or warm component. Prusa's [PLA guidance](https://help.prusa3d.com/article/pla_2062) describes its suitability for prototypes and its limited mechanical and temperature resistance. Check moving joints and loaded holders physically; keep the power-strip holder clear of heat and ventilation paths.

## Purchased material versus self-made parts

Print the drawers, enclosure, connectors, covers, labels, stands and holders from filament wherever the actual designs support it. List those parts and print quantities in an assembly inventory when their identities are confirmed. Do not charge for both the filament and a second purchased finished-part price for the same print.

Glue, fasteners, anti-slip feet and other extras are **not included as required purchases**. The design has not established that they are needed. Use an owned or genuinely free item only when appropriate for its job. If a non-printable component proves necessary and no suitable free source exists, flag that blocker rather than inventing an all-printed replacement or adding a paid part without agreement.

Items that the workstation holds, such as an existing enclosed power strip or tools, are not automatically purchases for Nexus. The abandoned lead-screw and padlock concepts are not included. Neither the printer nor the separate robot electronics is added to this draft.

## How to determine the filament amount

Slice the intended parts with the actual printer, orientation, layer height, walls, infill and supports. Sum the reported filament mass for the required print quantities. Include supports, brim and purge material where applicable, plus a separately stated allowance for test pieces and failed prints. Do not calculate a purchase quantity from the CAD bounding box or full-solid volume.

Use this calculation, separately for each material or colour actually needed:

```text
New filament needed (g) = max(0, planned sliced use + stated test/reprint allowance - confirmed usable stock)
Spools to buy = round up(new filament needed / grams per spool)
Purchase cost = spools to buy * actual price per spool
Cash needed = purchase cost + shipping + tax not already included
```

One colour is sufficient for an initial fit test; the CAD screenshot's colours do not require buying matching spools. Four uploaded exports do not establish a complete parts inventory. Two layouts exceed a 256 mm square bed in at least one current XY direction, so resolve printer fit before relying on a slice. Do not shrink connectors simply to force a fit.

For material-consumption accounting, `used grams / spool grams * spool price` is different from the cash cost of buying whole spools. Do not add both to the same purchasing total.

## What genuinely free means

Owned filament or hardware can be recorded as **already owned, no new purchase** once availability is confirmed. Donated items can be recorded as **donated, no new purchase** once arranged. That does not imply their replacement value is zero. Free printing also needs confirmation of who supplies filament and whether delivery has a cost. No such offer or inventory is assumed here.

Buying raw filament is consistent with fabricating the parts yourself. It does not make every underlying CAD design original: the existing [attribution record](../ATTRIBUTION.md) remains in place for reused models.

## Funding and sync status

The public [Half Life page](https://halflife.hackclub.com/) describes parts funding but does not establish that this project's filament is approved or that free printing is available. No funding application, purchase or platform BOM edit was made here.

These changes are on GitHub. The project already receives a Half Life sync, so check that a later sync has not replaced BOM.csv. Keep the same final quantities and quotes in the platform's BOM when submitting; this repository draft is not a substitute for that submission.
