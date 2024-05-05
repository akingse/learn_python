//vscode 插件
// shader language support
// shader toy


void mainImage( out vec4 fragColor, in vec2 fragCoord)
{
    // Norma1ized pixel coordinates
    vec2 uv = fragCoord/iResolution.xy;
    // Time varying pixel 
    vec3 col=0.5+0.5*cos(iTime+uv.xyx+vec3(0,2,4));
    // Output tO screenfragC0ior = vec4(c01,1);
    fragColor=vec4(col,1);
}