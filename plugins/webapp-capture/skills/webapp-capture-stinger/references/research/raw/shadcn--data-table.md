# Data Table

- URL: https://ui.shadcn.com/docs/components/data-table
- Fetched: 2026-09-15
- Source type: official docs (MDX from `apps/v4/content/docs/components/radix/data-table.mdx`, first ~330 of 903 lines transcribed), `shadcn-ui/ui` `main` branch
- Last updated (if shown): unknown. Frontmatter: `base: radix`, `component: true`, links to TanStack Table docs (https://tanstack.com/table/latest/docs/overview).

## Description

"Powerful table and datagrids built using TanStack Table."

## Introduction (per docs prose)

There is no single `data-table` shadcn component to install; the docs explicitly say: "Every data table or datagrid I've created has been unique... It doesn't make sense to combine all of these variations into a single component... So instead of a data-table component, I thought it would be more helpful to provide a guide on how to build your own." The guide starts from `<Table />` and builds a full data table using TanStack Table.

**Tip (per callout):** "If you find yourself using the same table in multiple places in your app, you can always extract it into a reusable component."

## Table of contents (as listed on the page)

Set up Table Features, Basic Table, Row Actions, Pagination, Sorting, Filtering, Visibility, Row Selection, Reusable Components.

## Installation

```bash
npx shadcn@latest add table
npm install @tanstack/react-table
```

**This guide uses TanStack Table v9.** This is a significant version note: TanStack Table v9 is feature-based (opt-in), a different API shape than the widely-known v8 `useReactTable`/`getCoreRowModel()` pattern.

## Prerequisites: example data shape

```tsx showLineNumbers
type Payment = {
  id: string
  amount: number
  status: "pending" | "processing" | "success" | "failed"
  email: string
}

export const payments: Payment[] = [
  {
    id: "728ed52f",
    amount: 100,
    status: "pending",
    email: "m@example.com",
  },
  {
    id: "489e1d42",
    amount: 125,
    status: "processing",
    email: "example@gmail.com",
  },
  // ...
]
```

## Project structure (Next.js example, framework-agnostic pattern)

```
app
└── payments
    ├── columns.tsx
    ├── data-table-features.ts
    ├── data-table.tsx
    └── page.tsx
```

- `columns.tsx` (client component): column definitions.
- `data-table-features.ts`: the shared `features` object telling TanStack Table which behavior to enable.
- `data-table.tsx` (client component): the `<DataTable />` component.
- `page.tsx` (server component): fetches data and renders the table.

## Set up Table Features (TanStack Table v9 opt-in model)

Per docs: "TanStack Table v9 is feature-based: you opt into the behavior you want, sorting, filtering, pagination, and so on, by declaring it with `tableFeatures()`. Anything you don't list is tree-shaken out of your bundle. That includes the built-in filter and sort functions: register the ones your columns rely on under `filterFns` and `sortFns`."

```tsx showLineNumbers title="app/payments/data-table-features.ts"
import {
  columnFilteringFeature,
  columnVisibilityFeature,
  createFilteredRowModel,
  createPaginatedRowModel,
  createSortedRowModel,
  filterFn_includesString,
  rowPaginationFeature,
  rowSelectionFeature,
  rowSortingFeature,
  sortFn_alphanumeric,
  sortFn_text,
  tableFeatures,
} from "@tanstack/react-table"

// New in v9: declare the features this table uses, anything you don't
// register is tree-shaken out of the bundle.
export const features = tableFeatures({
  columnFilteringFeature,
  columnVisibilityFeature,
  rowPaginationFeature,
  rowSelectionFeature,
  rowSortingFeature,
  filteredRowModel: createFilteredRowModel(),
  paginatedRowModel: createPaginatedRowModel(),
  sortedRowModel: createSortedRowModel(),
  filterFns: { includesString: filterFn_includesString },
  sortFns: { alphanumeric: sortFn_alphanumeric, text: sortFn_text },
})

// Pass this as the first generic argument to `ColumnDef`, `Column`, `Table`,
// and `Row` so each type knows which feature APIs are available.
export type DataTableFeatures = typeof features
```

**Note (per callout):** "The core row model is always included, so you never register it yourself. Row models for optional features are created with `create*RowModel()` and registered on the features object, there are no more `get*RowModel` table options."

## Basic Table

### Column definitions

```tsx showLineNumbers title="app/payments/columns.tsx"
"use client"

import { createColumnHelper } from "@tanstack/react-table"

import { type DataTableFeatures } from "./data-table-features"

// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
  id: string
  amount: number
  status: "pending" | "processing" | "success" | "failed"
  email: string
}

// Use `accessor` for data columns and `display` for columns without one.
const columnHelper = createColumnHelper<DataTableFeatures, Payment>()

export const columns = columnHelper.columns([
  columnHelper.accessor("status", {
    header: "Status",
  }),
  columnHelper.accessor("email", {
    header: "Email",
  }),
  columnHelper.accessor("amount", {
    header: "Amount",
  }),
])
```

**Note (per callout):** "Columns are where you define the core of what your table will look like. They define the data that will be displayed, how it will be formatted, sorted and filtered."

### `<DataTable />` component

```tsx showLineNumbers title="app/payments/data-table.tsx"
"use client"

import { useTable, type ColumnDef, type RowData } from "@tanstack/react-table"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

import { features, type DataTableFeatures } from "./data-table-features"

interface DataTableProps<TData extends RowData> {
  columns: ColumnDef<DataTableFeatures, TData>[]
  data: TData[]
}

export function DataTable<TData extends RowData>({
  columns,
  data,
}: DataTableProps<TData>) {
  const table = useTable({
    features,
    data,
    columns,
  })

  return (
    <div className="overflow-hidden rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead key={header.id}>
                    {header.isPlaceholder ? null : (
                      <table.FlexRender header={header} />
                    )}
                  </TableHead>
                )
              })}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow
                key={row.id}
                data-state={row.getIsSelected() && "selected"}
              >
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    <table.FlexRender cell={cell} />
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  )
}
```

**Tip (per callout):** if `<DataTable />` is used in multiple places, extract it to `components/ui/data-table.tsx`: `<DataTable columns={columns} data={data} />`.

**`<table.FlexRender />` vs `flexRender` (per callout):** "This guide uses v9's `<table.FlexRender header={header} />` and `<table.FlexRender cell={cell} />` component, available right on the table instance, no extra import needed. The classic `flexRender(component, context)` helper from v8 still works too, if you prefer the function form (or need to render outside the component that owns `table`, where you can also import the standalone `<FlexRender />`)."

### Render the table

```tsx showLineNumbers title="app/payments/page.tsx"
import { columns, Payment } from "./columns"
import { DataTable } from "./data-table"

async function getData(): Promise<Payment[]> {
  // Fetch data from your API here.
  return [
    {
      id: "728ed52f",
      amount: 100,
      status: "pending",
      email: "m@example.com",
    },
    // ...
  ]
}

export default async function DemoPage() {
  const data = await getData()

  return (
    <div className="container mx-auto py-10">
      <DataTable columns={columns} data={data} />
    </div>
  )
}
```

## Remaining sections (present on the page but not transcribed in this excerpt)

Row Actions, Pagination, Sorting, Filtering, Visibility, Row Selection, Reusable Components: all listed in the table of contents above; the full page (903 lines) continues with worked examples for each, following the same TanStack Table v9 `tableFeatures()` opt-in pattern shown above (e.g. registering `rowSelectionFeature`, `columnFilteringFeature` and rendering the corresponding UI: a filter `Input`, a `DropdownMenu` for column visibility, pagination `Button`s, a checkbox column for row selection). Re-fetch the full page for these sections if deeper detail is needed than the architecture already captured here.
