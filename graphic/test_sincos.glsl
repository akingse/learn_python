#define A(v) mat2(cos(m.v+radians(vec4(0, -90, 90, 0))))  // rotate
#define W(v) length(vec3(p.yz-v(p.x+vec2(0, pi_2)+t), 0))-lt  // wave
//#define W(v) length(p-vec3(round(p.x*pi)/pi, v(t+p.x), v(t+pi_2+p.x)))-lt  // wave
#define P(v) length(p-vec3(0, v(t), v(t+pi_2)))-pt  // point
void mainImage( out vec4 C, in vec2 U )
{
    float lt = .1, // line thickness
          pt = .3, // point thickness
          pi = 3.1416,
          pi2 = pi*2.,
          pi_2 = pi/2.,
          t = iTime*pi,
          s = 1., d = 0., i = d;
    vec2 R = iResolution.xy,
         m = (iMouse.xy-.5*R)/R.y*4.;
    vec3 o = vec3(0, 0, -7), // cam
         u = normalize(vec3((U-.5*R)/R.y, 1)),
         c = vec3(0), k = c, p;
    if (iMouse.z < 1.) m = -vec2(t/20.-pi_2, 0);
    mat2 v = A(y), h = A(x); // pitch & yaw
    for (; i++<50.;) // raymarch
    {
        p = o+u*d;
        p.yz *= v;
        p.xz *= h;
        p.x -= 3.;
        if (p.y < -1.5) p.y = 2./p.y;
        k.x = min( max(p.x+lt, W(sin)), P(sin) );
        k.y = min( max(p.x+lt, W(cos)), P(cos) );
        s = min(s, min(k.x, k.y));
        if (s < .001 || d > 100.) break;
        d += s*.5;
    }
    c = max(cos(d*pi2) - s*sqrt(d) - k, 0.);
    c.gb += .1;
    C = vec4(c*.4 + c.brg*.6 + c*c, 1);
}