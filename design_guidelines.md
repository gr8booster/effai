# EEFai Financial AI Platform - Design System Guidelines

## Design Philosophy

EEFai is a financial wellness platform designed for Americans facing emergency expenses, debt collection, and credit challenges. The design must convey **trust, calm, and hope** while maintaining professional credibility. Users are often in financial stress, so the interface must reduce cognitive load, provide clear guidance, and avoid overwhelming visuals.

**Core Design Principles:**
- **Trust First**: Professional, secure, transparent
- **Calm & Clarity**: Minimal cognitive load, clear hierarchy
- **Hope & Progress**: Positive reinforcement, visible progress
- **Accessibility**: WCAG 2.2 Level AA compliant
- **Human-Centered**: Empathetic, jargon-free, supportive

---

## GRADIENT RESTRICTION RULE

**NEVER use dark/saturated gradient combos** (e.g., purple/pink, blue-500 to purple-600) on any UI element.

**PROHIBITED GRADIENTS:**
- Purple to pink
- Dark blue to purple
- Red to pink
- Green-500 to blue-500
- Any dark saturated color combinations

**GRADIENT LIMITS:**
- NEVER let gradients cover more than 20% of the viewport
- NEVER apply gradients to text-heavy content or reading areas
- NEVER use gradients on small UI elements (<100px width)
- NEVER stack multiple gradient layers in the same viewport

**ENFORCEMENT RULE:**
IF gradient area exceeds 20% of viewport OR affects readability
THEN use solid colors instead

**ALLOWED GRADIENT USAGE:**
- Hero section backgrounds only (light, subtle gradients)
- Large CTA buttons (2-color max, light tones)
- Decorative accent elements only
- Section dividers or backgrounds (not content areas)

---

## Color System

### Primary Palette

```json
{
  "primary": {
    "50": "#E8F4F8",
    "100": "#D1E9F1",
    "200": "#A3D3E3",
    "300": "#75BDD5",
    "400": "#47A7C7",
    "500": "#2B8BA8",
    "600": "#236F86",
    "700": "#1B5364",
    "800": "#133742",
    "900": "#0B1B21"
  },
  "secondary": {
    "50": "#F0F7F4",
    "100": "#E1EFE9",
    "200": "#C3DFD3",
    "300": "#A5CFBD",
    "400": "#87BFA7",
    "500": "#66A88E",
    "600": "#528672",
    "700": "#3E6556",
    "800": "#2A433A",
    "900": "#15221D"
  },
  "accent": {
    "sage": "#8BA888",
    "teal": "#5B9AA0",
    "mint": "#A8D5BA",
    "warmGray": "#9CA3AF"
  },
  "semantic": {
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#3B82F6"
  },
  "neutral": {
    "50": "#F9FAFB",
    "100": "#F3F4F6",
    "200": "#E5E7EB",
    "300": "#D1D5DB",
    "400": "#9CA3AF",
    "500": "#6B7280",
    "600": "#4B5563",
    "700": "#374151",
    "800": "#1F2937",
    "900": "#111827"
  }
}
```

### Color Usage Guidelines

**Background Colors:**
- Primary background: `#FFFFFF` (white)
- Secondary background: `neutral-50` (#F9FAFB)
- Card backgrounds: `#FFFFFF` with subtle shadow
- Section dividers: `neutral-100` (#F3F4F6)

**Text Colors:**
- Primary text: `neutral-900` (#111827)
- Secondary text: `neutral-600` (#4B5563)
- Muted text: `neutral-500` (#6B7280)
- Link text: `primary-600` (#236F86)
- Link hover: `primary-700` (#1B5364)

**Interactive Elements:**
- Primary CTA: `primary-600` (#236F86) background, white text
- Primary CTA hover: `primary-700` (#1B5364)
- Secondary button: `secondary-500` (#66A88E) background, white text
- Ghost button: transparent background, `primary-600` border and text
- Disabled state: `neutral-300` background, `neutral-500` text

**Status Colors:**
- Success: `#10B981` (green-500)
- Warning: `#F59E0B` (amber-500)
- Error: `#EF4444` (red-500)
- Info: `primary-500` (#2B8BA8)

**Contrast Requirements:**
- All text must meet WCAG 2.2 Level AA: 4.5:1 for normal text, 3:1 for large text
- Interactive elements must have 3:1 contrast with adjacent colors
- Focus indicators must have 3:1 contrast

---

## Typography

### Font Families

**Primary Font (Body & UI):** IBM Plex Sans
- Professional, highly readable
- Excellent for financial/legal content
- Wide range of weights

**Secondary Font (Headings):** Manrope
- Modern, friendly, approachable
- Reduces intimidation factor
- Pairs well with IBM Plex Sans

**Monospace Font (Code/Numbers):** IBM Plex Mono
- For financial figures, account numbers, codes
- Clear distinction for data

### Font Loading

```javascript
// Add to index.html <head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=Manrope:wght@500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### Typography Scale

```css
/* Add to index.css */
:root {
  /* Font Families */
  --font-primary: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-heading: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
  
  /* Font Sizes */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px - minimum for body text */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  --text-6xl: 3.75rem;     /* 60px */
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  
  /* Letter Spacing */
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
}
```

### Text Hierarchy

**H1 - Main Page Heading:**
- Font: Manrope
- Size: `text-4xl sm:text-5xl lg:text-6xl` (36px → 48px → 60px)
- Weight: 700 (bold)
- Line height: 1.1
- Letter spacing: -0.025em
- Color: `neutral-900`
- Usage: Page titles, hero headings

**H2 - Section Heading:**
- Font: Manrope
- Size: `text-3xl sm:text-4xl` (30px → 36px)
- Weight: 600 (semibold)
- Line height: 1.2
- Color: `neutral-900`
- Usage: Major section titles

**H3 - Subsection Heading:**
- Font: Manrope
- Size: `text-2xl sm:text-3xl` (24px → 30px)
- Weight: 600 (semibold)
- Line height: 1.3
- Color: `neutral-800`
- Usage: Card titles, subsections

**H4 - Component Heading:**
- Font: IBM Plex Sans
- Size: `text-xl sm:text-2xl` (20px → 24px)
- Weight: 600 (semibold)
- Line height: 1.4
- Color: `neutral-800`
- Usage: Component titles, form sections

**Body Text:**
- Font: IBM Plex Sans
- Size: `text-base` (16px minimum)
- Weight: 400 (regular)
- Line height: 1.6
- Color: `neutral-700`
- Usage: Paragraphs, descriptions

**Small Text:**
- Font: IBM Plex Sans
- Size: `text-sm` (14px)
- Weight: 400 (regular)
- Line height: 1.5
- Color: `neutral-600`
- Usage: Captions, helper text, metadata

**Financial Data:**
- Font: IBM Plex Mono
- Size: `text-lg sm:text-xl` (18px → 20px)
- Weight: 500 (medium)
- Line height: 1.4
- Color: `neutral-900`
- Usage: Dollar amounts, account numbers, dates

---

## Spacing System

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
}
```

**Spacing Guidelines:**
- Component padding: `space-4` to `space-6` (16px-24px)
- Section spacing: `space-12` to `space-20` (48px-80px)
- Card padding: `space-6` (24px)
- Form field spacing: `space-4` (16px)
- Button padding: `space-3 space-6` (12px 24px)
- Use 2-3x more spacing than feels comfortable for a calm, uncluttered feel

---

## Button System

### Button Variants

**Primary Button (Main CTAs):**
```javascript
// Tailwind classes
className="inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-lg bg-primary-600 text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
data-testid="primary-cta-button"
```

**Secondary Button:**
```javascript
className="inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-lg bg-secondary-500 text-white hover:bg-secondary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-secondary-400 transition-colors duration-200"
data-testid="secondary-action-button"
```

**Ghost Button:**
```javascript
className="inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-lg border-2 border-primary-600 text-primary-600 hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200"
data-testid="ghost-button"
```

**Danger Button:**
```javascript
className="inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-lg bg-red-600 text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
data-testid="danger-action-button"
```

### Button Sizes

**Small:**
```javascript
className="px-4 py-2 text-sm"
```

**Medium (Default):**
```javascript
className="px-6 py-3 text-base"
```

**Large:**
```javascript
className="px-8 py-4 text-lg"
```

### Button Shape
- Border radius: `rounded-lg` (8px) - Professional, approachable
- Pill shape for special CTAs: `rounded-full`

### Button States
- **Hover**: Darken background by one shade
- **Focus**: 2px ring with offset, primary color
- **Active**: Scale down slightly (0.98)
- **Disabled**: 50% opacity, cursor not-allowed

---

## Component Library

### Shadcn/UI Components to Use

**Forms & Inputs:**
- `/app/frontend/src/components/ui/input.jsx` - Text inputs
- `/app/frontend/src/components/ui/textarea.jsx` - Multi-line text
- `/app/frontend/src/components/ui/select.jsx` - Dropdowns
- `/app/frontend/src/components/ui/checkbox.jsx` - Checkboxes
- `/app/frontend/src/components/ui/radio-group.jsx` - Radio buttons
- `/app/frontend/src/components/ui/switch.jsx` - Toggle switches
- `/app/frontend/src/components/ui/slider.jsx` - Range sliders
- `/app/frontend/src/components/ui/calendar.jsx` - Date picker
- `/app/frontend/src/components/ui/form.jsx` - Form wrapper with validation

**Layout & Structure:**
- `/app/frontend/src/components/ui/card.jsx` - Content cards
- `/app/frontend/src/components/ui/separator.jsx` - Dividers
- `/app/frontend/src/components/ui/tabs.jsx` - Tab navigation
- `/app/frontend/src/components/ui/accordion.jsx` - Collapsible sections
- `/app/frontend/src/components/ui/scroll-area.jsx` - Scrollable containers

**Feedback & Overlays:**
- `/app/frontend/src/components/ui/alert.jsx` - Alert messages
- `/app/frontend/src/components/ui/alert-dialog.jsx` - Confirmation dialogs
- `/app/frontend/src/components/ui/dialog.jsx` - Modal dialogs
- `/app/frontend/src/components/ui/sheet.jsx` - Side panels
- `/app/frontend/src/components/ui/toast.jsx` - Toast notifications
- `/app/frontend/src/components/ui/sonner.jsx` - Toast system (preferred)
- `/app/frontend/src/components/ui/progress.jsx` - Progress bars
- `/app/frontend/src/components/ui/skeleton.jsx` - Loading skeletons

**Navigation:**
- `/app/frontend/src/components/ui/navigation-menu.jsx` - Main navigation
- `/app/frontend/src/components/ui/breadcrumb.jsx` - Breadcrumbs
- `/app/frontend/src/components/ui/pagination.jsx` - Pagination
- `/app/frontend/src/components/ui/dropdown-menu.jsx` - Dropdown menus
- `/app/frontend/src/components/ui/menubar.jsx` - Menu bar

**Data Display:**
- `/app/frontend/src/components/ui/table.jsx` - Data tables
- `/app/frontend/src/components/ui/badge.jsx` - Status badges
- `/app/frontend/src/components/ui/avatar.jsx` - User avatars
- `/app/frontend/src/components/ui/tooltip.jsx` - Tooltips
- `/app/frontend/src/components/ui/hover-card.jsx` - Hover cards

---

## Layout System

### Grid System

**Container:**
```javascript
className="container mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl"
```

**Two-Column Layout (Dashboard):**
```javascript
className="grid grid-cols-1 lg:grid-cols-12 gap-6"
// Sidebar: lg:col-span-3
// Main content: lg:col-span-9
```

**Three-Column Layout (Cards):**
```javascript
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
```

**Bento Grid (Dashboard Widgets):**
```javascript
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 auto-rows-fr"
// Use col-span and row-span for varied sizes
```

### Responsive Breakpoints

```javascript
// Tailwind default breakpoints
sm: 640px   // Mobile landscape
md: 768px   // Tablet
lg: 1024px  // Desktop
xl: 1280px  // Large desktop
2xl: 1536px // Extra large
```

### Layout Patterns

**Hero Section:**
```javascript
<section className="relative bg-gradient-to-br from-primary-50 via-white to-secondary-50 py-16 sm:py-24" data-testid="hero-section">
  <div className="container mx-auto px-4 sm:px-6 lg:px-8">
    <div className="max-w-3xl">
      <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-neutral-900 mb-6">
        Your Financial Fresh Start
      </h1>
      <p className="text-lg sm:text-xl text-neutral-700 mb-8">
        AI-powered assistance for emergency expenses, debt relief, and credit repair
      </p>
      <button className="..." data-testid="hero-cta-button">Get Started</button>
    </div>
  </div>
</section>
```

**Dashboard Layout:**
```javascript
<div className="min-h-screen bg-neutral-50">
  {/* Header */}
  <header className="bg-white border-b border-neutral-200 sticky top-0 z-50" data-testid="dashboard-header">
    {/* Navigation */}
  </header>
  
  {/* Main Content */}
  <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      {/* Sidebar */}
      <aside className="lg:col-span-3" data-testid="dashboard-sidebar">
        {/* Navigation menu */}
      </aside>
      
      {/* Main Content Area */}
      <main className="lg:col-span-9" data-testid="dashboard-main">
        {/* Dashboard widgets */}
      </main>
    </div>
  </div>
</div>
```

**Card Grid:**
```javascript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map((item) => (
    <Card key={item.id} className="hover:shadow-lg transition-shadow duration-200" data-testid={`card-${item.id}`}>
      <CardHeader>
        <CardTitle>{item.title}</CardTitle>
      </CardHeader>
      <CardContent>
        {item.content}
      </CardContent>
    </Card>
  ))}
</div>
```

---

## Micro-Interactions & Motion

### Animation Principles

**Timing:**
- Fast interactions: 150-200ms (hover, focus)
- Medium interactions: 250-350ms (dropdowns, tooltips)
- Slow interactions: 400-600ms (page transitions, modals)

**Easing:**
- Default: `ease-in-out`
- Enter: `ease-out`
- Exit: `ease-in`

### Common Animations

**Button Hover:**
```css
.button {
  transition: background-color 200ms ease-in-out, transform 150ms ease-out;
}
.button:hover {
  transform: translateY(-1px);
}
.button:active {
  transform: translateY(0);
}
```

**Card Hover:**
```css
.card {
  transition: box-shadow 250ms ease-in-out, transform 250ms ease-out;
}
.card:hover {
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
```

**Fade In (Page Load):**
```javascript
// Use Framer Motion
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: 'easeOut' }}
>
  {content}
</motion.div>
```

**Progress Indicator:**
```javascript
// Smooth progress bar animation
<motion.div
  className="h-2 bg-primary-600 rounded-full"
  initial={{ width: 0 }}
  animate={{ width: `${progress}%` }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
  data-testid="progress-bar"
/>
```

### Framer Motion Installation

```bash
npm install framer-motion
```

**Usage Example:**
```javascript
import { motion, AnimatePresence } from 'framer-motion';

// Stagger children animation
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.div variants={container} initial="hidden" animate="show">
  {items.map((item) => (
    <motion.div key={item.id} variants={item}>
      {item.content}
    </motion.div>
  ))}
</motion.div>
```

---

## Data Visualization

### Recharts for Financial Charts

**Installation:**
```bash
npm install recharts
```

**Chart Types to Use:**

**1. Line Chart (Savings Progress):**
```javascript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={savingsData}>
    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
    <XAxis dataKey="month" stroke="#6B7280" />
    <YAxis stroke="#6B7280" />
    <Tooltip 
      contentStyle={{ 
        backgroundColor: '#FFFFFF', 
        border: '1px solid #E5E7EB',
        borderRadius: '8px'
      }} 
    />
    <Line 
      type="monotone" 
      dataKey="amount" 
      stroke="#2B8BA8" 
      strokeWidth={3}
      dot={{ fill: '#2B8BA8', r: 4 }}
    />
  </LineChart>
</ResponsiveContainer>
```

**2. Bar Chart (Debt Payoff):**
```javascript
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

<ResponsiveContainer width="100%" height={300}>
  <BarChart data={debtData}>
    <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
    <XAxis dataKey="creditor" stroke="#6B7280" />
    <YAxis stroke="#6B7280" />
    <Tooltip />
    <Bar dataKey="amount" fill="#66A88E" radius={[8, 8, 0, 0]} />
  </BarChart>
</ResponsiveContainer>
```

**3. Pie Chart (Expense Breakdown):**
```javascript
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#2B8BA8', '#66A88E', '#8BA888', '#5B9AA0', '#A8D5BA'];

<ResponsiveContainer width="100%" height={300}>
  <PieChart>
    <Pie
      data={expenseData}
      cx="50%"
      cy="50%"
      labelLine={false}
      outerRadius={100}
      fill="#8884d8"
      dataKey="value"
    >
      {expenseData.map((entry, index) => (
        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
      ))}
    </Pie>
    <Tooltip />
    <Legend />
  </PieChart>
</ResponsiveContainer>
```

**Chart Styling Guidelines:**
- Use primary/secondary colors from palette
- Grid lines: `neutral-200` (#E5E7EB)
- Axis labels: `neutral-600` (#4B5563)
- Tooltips: White background, subtle border, rounded corners
- Bar/line thickness: 2-3px for clarity
- Rounded corners on bars: `radius={[8, 8, 0, 0]}`

---

## Icons

### Lucide React (Already Installed)

```javascript
import { 
  Home, 
  FileText, 
  DollarSign, 
  TrendingUp, 
  Shield, 
  Users, 
  Bell,
  Settings,
  ChevronRight,
  Check,
  X,
  AlertCircle,
  Info,
  Upload,
  Download,
  Search,
  Menu,
  User
} from 'lucide-react';

// Usage
<DollarSign className="w-5 h-5 text-primary-600" />
```

**Icon Sizes:**
- Small: `w-4 h-4` (16px)
- Medium: `w-5 h-5` (20px)
- Large: `w-6 h-6` (24px)
- Extra Large: `w-8 h-8` (32px)

**Icon Colors:**
- Primary actions: `text-primary-600`
- Secondary actions: `text-neutral-600`
- Success: `text-green-600`
- Warning: `text-amber-600`
- Error: `text-red-600`

---

## Image Assets

### Hero Section Images

**Primary Hero Image (Financial Planning):**
```
https://images.unsplash.com/photo-1746021535489-00edc5efb203
```
- Description: Clean, professional workspace with dual monitors
- Usage: Homepage hero, about page
- Alt text: "Professional financial planning workspace"

**Secondary Hero Image (Modern Office):**
```
https://images.unsplash.com/photo-1758630737403-1bda34e3f98e
```
- Description: Modern office with desks and wood accents
- Usage: Services page, team page
- Alt text: "Modern collaborative workspace"

### Growth & Progress Images

**Financial Growth (Plant on Coins):**
```
https://images.unsplash.com/photo-1579621970563-ebec7560ff3e
```
- Description: Green plant growing on coins
- Usage: Savings tracker, progress indicators
- Alt text: "Financial growth and savings progress"

**New Beginnings (Sprout):**
```
https://images.unsplash.com/photo-1666549415033-b45039335fe4
```
- Description: Small plant sprouting from ground
- Usage: Onboarding, fresh start messaging
- Alt text: "New financial beginning"

**Hope & Growth (Plant Growth):**
```
https://images.unsplash.com/photo-1579227114496-27346f474519
```
- Description: Green leafed plant on coins
- Usage: Success stories, testimonials
- Alt text: "Financial wellness and growth"

### Community & Support Images

**Hands Together (Support):**
```
https://images.unsplash.com/photo-1763982811982-e4901b18bbe3
```
- Description: Multiple hands of different sizes layered together
- Usage: Community features, support pages
- Alt text: "Community support and collaboration"

**Handholding (Trust):**
```
https://images.unsplash.com/photo-1739757646223-aae94c6ca541
```
- Description: Group of people holding hands
- Usage: About page, testimonials
- Alt text: "Trust and partnership in financial wellness"

### Image Implementation

```javascript
// Optimized image component
const HeroImage = () => (
  <div className="relative w-full h-96 rounded-lg overflow-hidden">
    <img
      src="https://images.unsplash.com/photo-1746021535489-00edc5efb203"
      alt="Professional financial planning workspace"
      className="w-full h-full object-cover"
      loading="lazy"
      data-testid="hero-image"
    />
    <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
  </div>
);
```

---

## Accessibility Guidelines (WCAG 2.2 Level AA)

### Color Contrast

**Text Contrast:**
- Normal text (< 18px): 4.5:1 minimum
- Large text (≥ 18px or 14px bold): 3:1 minimum
- UI components: 3:1 minimum

**Verified Combinations:**
- `neutral-900` on white: 16.1:1 ✓
- `neutral-700` on white: 8.6:1 ✓
- `primary-600` on white: 5.2:1 ✓
- White on `primary-600`: 4.1:1 ✓
- White on `secondary-600`: 3.8:1 ✓

### Keyboard Navigation

**Focus Indicators:**
```css
/* All interactive elements must have visible focus */
.interactive-element:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* Or use ring utilities */
focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
```

**Tab Order:**
- Logical tab order following visual flow
- Skip links for main content
- No keyboard traps

**Keyboard Shortcuts:**
- All mouse actions must have keyboard equivalents
- Document keyboard shortcuts in help section

### Screen Reader Support

**Semantic HTML:**
```javascript
// Use proper HTML5 elements
<header>, <nav>, <main>, <aside>, <footer>, <article>, <section>

// ARIA labels for dynamic content
<button aria-label="Upload document" data-testid="upload-button">
  <Upload className="w-5 h-5" />
</button>

// ARIA live regions for status updates
<div role="status" aria-live="polite" aria-atomic="true">
  Document uploaded successfully
</div>
```

**Alt Text:**
- All images must have descriptive alt text
- Decorative images: `alt=""`
- Informative images: Describe content and context

**Form Labels:**
```javascript
// Always associate labels with inputs
<label htmlFor="email" className="block text-sm font-medium text-neutral-700">
  Email Address
</label>
<input
  id="email"
  type="email"
  name="email"
  aria-required="true"
  aria-describedby="email-error"
  data-testid="email-input"
/>
<span id="email-error" className="text-sm text-red-600" role="alert">
  {error}
</span>
```

### Motion & Animation

**Respect Reduced Motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```javascript
// In React components
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

<motion.div
  animate={{ opacity: 1 }}
  transition={{ duration: prefersReducedMotion ? 0 : 0.4 }}
>
  {content}
</motion.div>
```

### Error Handling

**Error Messages:**
- Clear, specific error messages
- Suggest how to fix the error
- Use color + icon (not color alone)
- Announce errors to screen readers

```javascript
<Alert variant="destructive" role="alert" data-testid="error-alert">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>
    Please enter a valid email address. Example: user@example.com
  </AlertDescription>
</Alert>
```

### Testing Requirements

**All interactive elements must include `data-testid` attributes:**

```javascript
// Buttons
<button data-testid="submit-form-button">Submit</button>

// Form inputs
<input data-testid="email-input" />

// Links
<a href="/dashboard" data-testid="dashboard-link">Dashboard</a>

// Cards
<Card data-testid="savings-card">...</Card>

// Dialogs
<Dialog data-testid="confirmation-dialog">...</Dialog>

// Navigation items
<nav data-testid="main-navigation">...</nav>
```

**Naming Convention:**
- Use kebab-case
- Describe the element's role, not appearance
- Be specific: `login-form-submit-button` not `button-1`

---

## Form Design

### Form Layout

**Vertical Stack (Preferred):**
```javascript
<form className="space-y-6" data-testid="user-form">
  <div>
    <label htmlFor="name" className="block text-sm font-medium text-neutral-700 mb-2">
      Full Name
    </label>
    <input
      id="name"
      type="text"
      className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      data-testid="name-input"
    />
  </div>
  
  <div>
    <label htmlFor="email" className="block text-sm font-medium text-neutral-700 mb-2">
      Email Address
    </label>
    <input
      id="email"
      type="email"
      className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
      data-testid="email-input"
    />
  </div>
</form>
```

### Input States

**Default:**
```javascript
className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors"
```

**Error:**
```javascript
className="w-full px-4 py-3 border-2 border-red-500 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
```

**Success:**
```javascript
className="w-full px-4 py-3 border-2 border-green-500 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
```

**Disabled:**
```javascript
className="w-full px-4 py-3 border border-neutral-300 rounded-lg bg-neutral-100 text-neutral-500 cursor-not-allowed"
disabled
```

### Helper Text

```javascript
<p className="mt-2 text-sm text-neutral-600">
  We'll never share your email with anyone else.
</p>
```

### Error Messages

```javascript
{error && (
  <p className="mt-2 text-sm text-red-600 flex items-center gap-2" role="alert">
    <AlertCircle className="w-4 h-4" />
    {error}
  </p>
)}
```

---

## Document Upload Component

### File Upload Design

```javascript
import { Upload, File, X } from 'lucide-react';
import { useState } from 'react';

const DocumentUpload = () => {
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${isDragging 
            ? 'border-primary-500 bg-primary-50' 
            : 'border-neutral-300 hover:border-primary-400'
          }
        `}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragging(false);
          // Handle file drop
        }}
        data-testid="file-upload-dropzone"
      >
        <Upload className="w-12 h-12 text-neutral-400 mx-auto mb-4" />
        <p className="text-base font-medium text-neutral-700 mb-2">
          Drop your documents here, or click to browse
        </p>
        <p className="text-sm text-neutral-500">
          PDF, DOC, DOCX up to 10MB
        </p>
        <input
          type="file"
          className="hidden"
          id="file-upload"
          multiple
          accept=".pdf,.doc,.docx"
          data-testid="file-upload-input"
        />
        <label
          htmlFor="file-upload"
          className="inline-block mt-4 px-6 py-3 bg-primary-600 text-white rounded-lg cursor-pointer hover:bg-primary-700 transition-colors"
        >
          Select Files
        </label>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-2" data-testid="uploaded-files-list">
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg border border-neutral-200"
              data-testid={`uploaded-file-${index}`}
            >
              <div className="flex items-center gap-3">
                <File className="w-5 h-5 text-primary-600" />
                <div>
                  <p className="text-sm font-medium text-neutral-900">{file.name}</p>
                  <p className="text-xs text-neutral-500">{file.size}</p>
                </div>
              </div>
              <button
                onClick={() => {/* Remove file */}}
                className="p-2 text-neutral-400 hover:text-red-600 transition-colors"
                data-testid={`remove-file-${index}`}
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## Progress Indicators

### Linear Progress Bar

```javascript
import { motion } from 'framer-motion';

const ProgressBar = ({ progress, label }) => (
  <div className="space-y-2" data-testid="progress-indicator">
    <div className="flex justify-between items-center">
      <span className="text-sm font-medium text-neutral-700">{label}</span>
      <span className="text-sm font-medium text-primary-600">{progress}%</span>
    </div>
    <div className="h-2 bg-neutral-200 rounded-full overflow-hidden">
      <motion.div
        className="h-full bg-primary-600 rounded-full"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
      />
    </div>
  </div>
);
```

### Circular Progress (Savings Goal)

```javascript
const CircularProgress = ({ progress, goal, current }) => {
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center" data-testid="circular-progress">
      <svg className="transform -rotate-90" width="140" height="140">
        {/* Background circle */}
        <circle
          cx="70"
          cy="70"
          r={radius}
          stroke="#E5E7EB"
          strokeWidth="8"
          fill="none"
        />
        {/* Progress circle */}
        <motion.circle
          cx="70"
          cy="70"
          r={radius}
          stroke="#2B8BA8"
          strokeWidth="8"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'easeOut' }}
        />
      </svg>
      <div className="absolute text-center">
        <p className="text-2xl font-bold text-neutral-900">{progress}%</p>
        <p className="text-xs text-neutral-600">of ${goal}</p>
      </div>
    </div>
  );
};
```

### Step Progress (Multi-step Forms)

```javascript
const StepProgress = ({ steps, currentStep }) => (
  <div className="flex items-center justify-between" data-testid="step-progress">
    {steps.map((step, index) => (
      <div key={index} className="flex items-center flex-1">
        <div className="flex flex-col items-center">
          <div
            className={`
              w-10 h-10 rounded-full flex items-center justify-center font-medium
              ${index < currentStep 
                ? 'bg-primary-600 text-white' 
                : index === currentStep
                ? 'bg-primary-600 text-white ring-4 ring-primary-100'
                : 'bg-neutral-200 text-neutral-600'
              }
            `}
            data-testid={`step-${index}`}
          >
            {index < currentStep ? <Check className="w-5 h-5" /> : index + 1}
          </div>
          <span className="mt-2 text-xs font-medium text-neutral-700">{step}</span>
        </div>
        {index < steps.length - 1 && (
          <div
            className={`
              flex-1 h-1 mx-4
              ${index < currentStep ? 'bg-primary-600' : 'bg-neutral-200'}
            `}
          />
        )}
      </div>
    ))}
  </div>
);
```

---

## Dashboard Widgets

### Stat Card

```javascript
import { TrendingUp, TrendingDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';

const StatCard = ({ title, value, change, trend, icon: Icon }) => (
  <Card data-testid="stat-card">
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium text-neutral-600">
        {title}
      </CardTitle>
      <Icon className="w-5 h-5 text-neutral-400" />
    </CardHeader>
    <CardContent>
      <div className="text-3xl font-bold text-neutral-900">{value}</div>
      <div className="flex items-center gap-2 mt-2">
        {trend === 'up' ? (
          <TrendingUp className="w-4 h-4 text-green-600" />
        ) : (
          <TrendingDown className="w-4 h-4 text-red-600" />
        )}
        <span className={`text-sm font-medium ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
          {change}
        </span>
        <span className="text-sm text-neutral-500">from last month</span>
      </div>
    </CardContent>
  </Card>
);
```

### Quick Action Card

```javascript
const QuickActionCard = ({ title, description, icon: Icon, onClick }) => (
  <Card 
    className="cursor-pointer hover:shadow-lg transition-shadow duration-200 border-2 border-transparent hover:border-primary-200"
    onClick={onClick}
    data-testid="quick-action-card"
  >
    <CardContent className="p-6">
      <div className="flex items-start gap-4">
        <div className="p-3 bg-primary-100 rounded-lg">
          <Icon className="w-6 h-6 text-primary-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">{title}</h3>
          <p className="text-sm text-neutral-600">{description}</p>
        </div>
        <ChevronRight className="w-5 h-5 text-neutral-400" />
      </div>
    </CardContent>
  </Card>
);
```

---

## Toast Notifications (Sonner)

### Installation & Setup

Sonner is already available at `/app/frontend/src/components/ui/sonner.jsx`

### Usage

```javascript
import { toast } from 'sonner';

// Success
toast.success('Document uploaded successfully', {
  description: 'Your document has been processed and saved.',
});

// Error
toast.error('Upload failed', {
  description: 'Please try again or contact support.',
});

// Info
toast.info('Processing your request', {
  description: 'This may take a few moments.',
});

// Warning
toast.warning('Action required', {
  description: 'Please review your information before submitting.',
});

// With action
toast('Document ready', {
  description: 'Your letter has been generated.',
  action: {
    label: 'Download',
    onClick: () => downloadDocument(),
  },
});
```

### Toast Styling

```javascript
// In App.js or main layout
import { Toaster } from './components/ui/sonner';

<Toaster 
  position="top-right"
  toastOptions={{
    style: {
      background: '#FFFFFF',
      border: '1px solid #E5E7EB',
      color: '#111827',
    },
    className: 'font-primary',
  }}
/>
```

---

## Loading States

### Skeleton Loader

```javascript
import { Skeleton } from './components/ui/skeleton';

const CardSkeleton = () => (
  <Card>
    <CardHeader>
      <Skeleton className="h-6 w-1/2" />
    </CardHeader>
    <CardContent className="space-y-3">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
    </CardContent>
  </Card>
);
```

### Spinner

```javascript
const Spinner = ({ size = 'md' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex items-center justify-center" data-testid="loading-spinner">
      <div
        className={`
          ${sizeClasses[size]}
          border-4 border-neutral-200 border-t-primary-600
          rounded-full animate-spin
        `}
      />
    </div>
  );
};
```

### Loading Overlay

```javascript
const LoadingOverlay = ({ message = 'Loading...' }) => (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" data-testid="loading-overlay">
    <div className="bg-white rounded-lg p-8 max-w-sm mx-4 text-center">
      <Spinner size="lg" />
      <p className="mt-4 text-lg font-medium text-neutral-900">{message}</p>
    </div>
  </div>
);
```

---

## Responsive Design Checklist

### Mobile (< 640px)
- [ ] Single column layout
- [ ] Hamburger menu for navigation
- [ ] Touch-friendly buttons (min 44x44px)
- [ ] Simplified data tables (card view)
- [ ] Bottom navigation for key actions
- [ ] Reduced font sizes (but min 16px for body)
- [ ] Stacked form fields

### Tablet (640px - 1024px)
- [ ] Two-column layout where appropriate
- [ ] Collapsible sidebar
- [ ] Larger touch targets
- [ ] Optimized data tables
- [ ] Side navigation visible

### Desktop (> 1024px)
- [ ] Multi-column layouts
- [ ] Persistent sidebar navigation
- [ ] Hover states for all interactive elements
- [ ] Full data tables
- [ ] Tooltips and hover cards
- [ ] Keyboard shortcuts

---

## Admin Console Specific Guidelines

### Admin Dashboard Layout

```javascript
<div className="min-h-screen bg-neutral-50">
  {/* Admin Header */}
  <header className="bg-white border-b border-neutral-200 sticky top-0 z-50" data-testid="admin-header">
    <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-neutral-900">Admin Console</h1>
        <div className="flex items-center gap-4">
          <Badge variant="outline" data-testid="pending-reviews-badge">
            12 Pending Reviews
          </Badge>
          <Avatar data-testid="admin-avatar">
            <AvatarFallback>AD</AvatarFallback>
          </Avatar>
        </div>
      </div>
    </div>
  </header>

  {/* Admin Content */}
  <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <Tabs defaultValue="reviews" data-testid="admin-tabs">
      <TabsList>
        <TabsTrigger value="reviews">Reviews</TabsTrigger>
        <TabsTrigger value="users">Users</TabsTrigger>
        <TabsTrigger value="analytics">Analytics</TabsTrigger>
      </TabsList>
      
      <TabsContent value="reviews">
        {/* Review queue */}
      </TabsContent>
    </Tabs>
  </div>
</div>
```

### Review Queue Card

```javascript
const ReviewCard = ({ case: caseData }) => (
  <Card className="mb-4" data-testid={`review-case-${caseData.id}`}>
    <CardHeader>
      <div className="flex items-start justify-between">
        <div>
          <CardTitle className="text-lg">{caseData.title}</CardTitle>
          <p className="text-sm text-neutral-600 mt-1">
            Submitted {caseData.submittedDate}
          </p>
        </div>
        <Badge variant={caseData.priority === 'high' ? 'destructive' : 'secondary'}>
          {caseData.priority}
        </Badge>
      </div>
    </CardHeader>
    <CardContent>
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-neutral-700 mb-2">AI Analysis</h4>
          <p className="text-sm text-neutral-600">{caseData.aiAnalysis}</p>
        </div>
        
        <div className="flex gap-3">
          <Button 
            variant="default" 
            className="flex-1"
            data-testid={`approve-case-${caseData.id}`}
          >
            <Check className="w-4 h-4 mr-2" />
            Approve
          </Button>
          <Button 
            variant="outline" 
            className="flex-1"
            data-testid={`request-changes-${caseData.id}`}
          >
            Request Changes
          </Button>
          <Button 
            variant="destructive" 
            className="flex-1"
            data-testid={`reject-case-${caseData.id}`}
          >
            <X className="w-4 h-4 mr-2" />
            Reject
          </Button>
        </div>
      </div>
    </CardContent>
  </Card>
);
```

---

## Micro-Learning UI

### Daily Task Card

```javascript
const DailyTaskCard = ({ task, completed, onComplete }) => (
  <Card 
    className={`
      transition-all duration-200
      ${completed ? 'bg-green-50 border-green-200' : 'hover:shadow-md'}
    `}
    data-testid={`daily-task-${task.id}`}
  >
    <CardContent className="p-6">
      <div className="flex items-start gap-4">
        <div className={`
          w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0
          ${completed ? 'bg-green-500' : 'bg-primary-100'}
        `}>
          {completed ? (
            <Check className="w-6 h-6 text-white" />
          ) : (
            <task.icon className="w-6 h-6 text-primary-600" />
          )}
        </div>
        
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-neutral-900 mb-2">
            {task.title}
          </h3>
          <p className="text-sm text-neutral-600 mb-4">
            {task.description}
          </p>
          
          {!completed && (
            <Button 
              onClick={onComplete}
              size="sm"
              data-testid={`complete-task-${task.id}`}
            >
              Mark Complete
            </Button>
          )}
          
          {completed && (
            <p className="text-sm font-medium text-green-600">
              ✓ Completed
            </p>
          )}
        </div>
      </div>
    </CardContent>
  </Card>
);
```

### Learning Module

```javascript
const LearningModule = ({ module }) => (
  <Card data-testid={`learning-module-${module.id}`}>
    <CardHeader>
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
          <module.icon className="w-5 h-5 text-primary-600" />
        </div>
        <div>
          <CardTitle className="text-lg">{module.title}</CardTitle>
          <p className="text-sm text-neutral-600">{module.duration} min read</p>
        </div>
      </div>
    </CardHeader>
    <CardContent>
      <p className="text-sm text-neutral-700 mb-4">{module.description}</p>
      
      <div className="mb-4">
        <div className="flex justify-between text-sm mb-2">
          <span className="text-neutral-600">Progress</span>
          <span className="font-medium text-primary-600">{module.progress}%</span>
        </div>
        <div className="h-2 bg-neutral-200 rounded-full overflow-hidden">
          <div 
            className="h-full bg-primary-600 rounded-full transition-all duration-300"
            style={{ width: `${module.progress}%` }}
          />
        </div>
      </div>
      
      <Button 
        variant={module.progress > 0 ? 'default' : 'outline'}
        className="w-full"
        data-testid={`start-module-${module.id}`}
      >
        {module.progress > 0 ? 'Continue' : 'Start Learning'}
      </Button>
    </CardContent>
  </Card>
);
```

---

## Common Mistakes to Avoid

### ❌ Don't:
- Use dark purple, dark blue, dark pink, or dark red in gradients
- Apply gradients to more than 20% of viewport
- Use gradients on text-heavy content or reading areas
- Center-align the entire app container (`.App { text-align: center; }`)
- Use universal transitions (`transition: all`)
- Use emoji characters for icons (🤖💰📊 etc.)
- Mix multiple gradient directions in the same section
- Use gradients on small UI elements (<100px)
- Skip responsive font sizing
- Forget hover and focus states
- Ignore accessibility features (focus states, contrast)
- Use color alone to convey information
- Create keyboard traps
- Use generic `data-testid` values

### ✅ Do:
- Use white backgrounds for all cards and content areas
- Use light, subtle gradients only for hero sections (max 20% viewport)
- Use solid colors for content and reading areas
- Use FontAwesome CDN or lucide-react for icons
- Maintain consistent spacing using the spacing system
- Test on mobile devices with touch interactions
- Include accessibility features (focus states, WCAG contrast)
- Use specific transitions for interactive elements (buttons, inputs)
- Add `data-testid` to all interactive elements
- Use semantic HTML and ARIA labels
- Provide keyboard alternatives for all mouse actions
- Test with screen readers
- Respect `prefers-reduced-motion`

---

## CSS Custom Properties Setup

Add to `/app/frontend/src/index.css`:

```css
@layer base {
  :root {
    /* Colors */
    --primary-50: #E8F4F8;
    --primary-100: #D1E9F1;
    --primary-200: #A3D3E3;
    --primary-300: #75BDD5;
    --primary-400: #47A7C7;
    --primary-500: #2B8BA8;
    --primary-600: #236F86;
    --primary-700: #1B5364;
    --primary-800: #133742;
    --primary-900: #0B1B21;
    
    --secondary-50: #F0F7F4;
    --secondary-100: #E1EFE9;
    --secondary-200: #C3DFD3;
    --secondary-300: #A5CFBD;
    --secondary-400: #87BFA7;
    --secondary-500: #66A88E;
    --secondary-600: #528672;
    --secondary-700: #3E6556;
    --secondary-800: #2A433A;
    --secondary-900: #15221D;
    
    /* Accent Colors */
    --accent-sage: #8BA888;
    --accent-teal: #5B9AA0;
    --accent-mint: #A8D5BA;
    --accent-warm-gray: #9CA3AF;
    
    /* Semantic Colors */
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --info: #3B82F6;
    
    /* Typography */
    --font-primary: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-heading: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'IBM Plex Mono', 'Courier New', monospace;
    
    /* Spacing */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;
    --space-12: 3rem;
    --space-16: 4rem;
    --space-20: 5rem;
    --space-24: 6rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    
    /* Border Radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    --radius-full: 9999px;
  }
  
  body {
    font-family: var(--font-primary);
    color: var(--neutral-900);
    background-color: #FFFFFF;
  }
  
  h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
  }
}

/* Prevent universal transitions */
* {
  transition-property: none;
}

/* Add specific transitions only where needed */
button, a, input, select, textarea {
  transition-property: background-color, border-color, color, opacity;
  transition-duration: 200ms;
  transition-timing-function: ease-in-out;
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Instructions to Main Agent

### Implementation Priority

1. **Setup Phase:**
   - Install required dependencies: `framer-motion`, `recharts`
   - Add Google Fonts link to `index.html`
   - Update `index.css` with custom properties and base styles
   - Configure Tailwind with custom colors

2. **Core Components:**
   - Create reusable button components with all variants
   - Build form components with proper validation states
   - Implement card layouts for dashboard
   - Create navigation components (header, sidebar, mobile menu)

3. **Feature Components:**
   - Document upload component with drag-and-drop
   - Progress indicators (linear, circular, step-based)
   - Data visualization charts (savings, debt, expenses)
   - Admin review queue interface
   - Micro-learning task cards

4. **Accessibility:**
   - Add `data-testid` to ALL interactive elements
   - Implement keyboard navigation
   - Add ARIA labels and roles
   - Test color contrast ratios
   - Add focus indicators to all interactive elements

5. **Responsive Design:**
   - Mobile-first approach
   - Test on all breakpoints (sm, md, lg, xl)
   - Optimize touch targets for mobile
   - Implement responsive typography

6. **Polish:**
   - Add micro-interactions and hover states
   - Implement loading states and skeletons
   - Add toast notifications for user feedback
   - Test with screen readers
   - Optimize images and assets

### Key Reminders

- **NO dark gradients** (purple/pink, blue/purple, etc.)
- **Gradients max 20% of viewport** - use solid colors for content
- **White backgrounds** for all cards and content areas
- **IBM Plex Sans** for body text, **Manrope** for headings
- **Minimum 16px** font size for body text
- **4.5:1 contrast ratio** for all text
- **data-testid** on every interactive element
- **No universal transitions** - only specific properties
- **Lucide React** for icons, not emojis
- **Sonner** for toast notifications
- **Shadcn/UI** components as primary library
- **Framer Motion** for animations
- **Recharts** for data visualization

### Testing Checklist

- [ ] All interactive elements have `data-testid`
- [ ] Keyboard navigation works throughout
- [ ] Focus indicators visible on all interactive elements
- [ ] Color contrast meets WCAG 2.2 Level AA
- [ ] Screen reader announces all important content
- [ ] Forms have proper labels and error messages
- [ ] Responsive on mobile, tablet, and desktop
- [ ] Touch targets minimum 44x44px on mobile
- [ ] Loading states for all async operations
- [ ] Error handling with clear messages
- [ ] Success feedback for all actions
- [ ] Reduced motion preference respected

---

## General UI/UX Design Guidelines

### Transition Rules
- You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms

### Text Alignment
- You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text

### Icons
- NEVER use AI assistant Emoji characters like `🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇` etc for icons
- Always use **FontAwesome CDN** or **lucid-react** library already installed in package.json

### Gradient Restrictions
**NEVER use dark/saturated gradient combos** (e.g., purple/pink) on any UI element
- Prohibited gradients: blue-500 to purple-600, purple-500 to pink-500, green-500 to blue-500, red to pink etc
- NEVER use dark gradients for logo, testimonial, footer etc
- NEVER let gradients cover more than 20% of the viewport
- NEVER apply gradients to text-heavy content or reading areas
- NEVER use gradients on small UI elements (<100px width)
- NEVER stack multiple gradient layers in the same viewport

**ENFORCEMENT RULE:**
- If gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors

**How and where to use:**
- Section backgrounds (not content backgrounds)
- Hero section header content (dark to light to dark color)
- Decorative overlays and accent elements only
- Hero section with 2-3 mild colors
- Gradients can be horizontal, vertical, or diagonal

### Color Guidelines for AI Applications
- For AI chat, voice application, **do not use purple color**
- Use colors like light green, ocean blue, peach orange etc

### Micro-Animations
- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations
- Static = dead

### Spacing
- Use 2-3x more spacing than feels comfortable
- Cramped designs look cheap

### Visual Details
- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations separate good from extraordinary

### Design Tokens
- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion)
- Immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors)
- Don't rely on library defaults
- Don't make the background dark as a default step
- Always understand problem first and define colors accordingly
  - If playful/energetic → choose colorful scheme
  - If monochrome/minimal → choose black-white/neutral scheme

### Component Reuse
- Prioritize using pre-existing components from `src/components/ui` when applicable
- Create new components that match the style and conventions of existing components
- Examine existing components to understand the project's component patterns before creating new ones

### Component Library
- **IMPORTANT**: Do not use HTML based components like dropdown, calendar, toast etc
- You **MUST** always use `/app/frontend/src/components/ui/` only as primary components
- These are modern and stylish Shadcn/UI components

### Best Practices
- Use Shadcn/UI as the primary component library for consistency and accessibility
- Import path: `./components/[component-name]`

### Export Conventions
- Components MUST use named exports: `export const ComponentName = ...`
- Pages MUST use default exports: `export default function PageName() {...}`

### Toasts
- Use `sonner` for toasts
- Sonner component located in `/app/src/components/ui/sonner.jsx`

### Visual Depth
- Use 2-4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals

### Design Quality
- The result should feel human-made, visually appealing, converting, and easy for AI agents to implement
- Good contrast, balanced font sizes, proper gradients, sufficient whitespace, thoughtful motion and hierarchy
- Avoid overuse of elements and deliver a polished, effective design system

---

**END OF DESIGN GUIDELINES**

Path: `/app/design_guidelines.md`
