import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const url = request.nextUrl
  const pathname = url.pathname

  // Teljesen publikus útvonalak – bárki láthatja
  const publicPaths = ['/', '/manufacturer', '/business-buyer', '/individual-buyer', '/builder']

  if (publicPaths.includes(pathname) || publicPaths.some(p => pathname.startsWith(p + '/'))) {
    return NextResponse.next()
  }

  // Minden más útvonal (signup, login, dashboard, builder-próba stb.) védett
  const secret = url.searchParams.get('secret')

  // Rejtett kulcs – csak ezzel jutsz be (cseréld ki saját titkos kulcsra!)
  if (secret === 'nexustitkos2026') {
    return NextResponse.next()
  }

  // Ha nincs secret → redirect a főoldalra (senki nem jut tovább)
  return NextResponse.redirect(new URL('/', request.url))
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
