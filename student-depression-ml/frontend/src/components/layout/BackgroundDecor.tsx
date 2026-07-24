/**
 * Fixed, blurred color blobs behind all page content. Glassmorphism panels
 * (see .glass in index.css) need something colorful underneath to actually
 * read as "frosted glass" — over a flat background the blur has nothing to
 * bend and just looks like dull gray.
 */
export function BackgroundDecor() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute -top-24 -left-24 h-96 w-96 rounded-full bg-sage-100 opacity-70 blur-3xl" />
      <div className="absolute top-1/3 -right-32 h-[28rem] w-[28rem] rounded-full bg-peach-100 opacity-70 blur-3xl" />
      <div className="absolute bottom-0 left-1/4 h-80 w-80 rounded-full bg-terracotta-100 opacity-50 blur-3xl" />
    </div>
  );
}
