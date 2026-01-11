
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { PopularAuthor, ProjectionPoint, WordCloudItem } from '../types';

export const PopularAuthorsChart: React.FC<{ data: PopularAuthor[] }> = ({ data }) => {
  const COLORS = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe'];
  const BAR_HEIGHT = 28 * 2;
  const MAX_HEIGHT = 400;

  const chartHeight = Math.min(
    data.length * BAR_HEIGHT,
    MAX_HEIGHT
  );

  return (
    <div className="w-full bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="text-lg font-bold mb-6 text-slate-800">Popular Authors</h3>
      <div style={{ width: '100%', height: `${chartHeight}px` }}>
        <ResponsiveContainer width="100%" height={chartHeight}>
          <BarChart
            data={data}
            layout="vertical"
            barSize={BAR_HEIGHT}
            margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#f1f5f9" />
            <XAxis type="number" hide />
            <YAxis 
              dataKey="author" 
              type="category" 
              width={120} 
              tick={{ fill: '#64748b', fontSize: 12 }} 
            />
            <Tooltip 
              cursor={{ fill: '#f8fafc' }}
              contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            />
            <Bar dataKey="post_count" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};


function formatTooltip(d: ProjectionPoint): string {
  const topKeywords = d.keywords
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map(k => k.keyword)
    .join(", ");
  return `Post ID: ${d.post_id}<br>Top keywords: ${topKeywords}`;
}


export const PostProjectionMap: React.FC<{ data: ProjectionPoint[] }> = ({ data }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || data.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const width = 800;
    const height = 400;
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };

    const xExtent = d3.extent(data, d => d.x) as [number, number];
    const yExtent = d3.extent(data, d => d.y) as [number, number];

    const xScale = d3.scaleLinear().domain(xExtent).range([margin.left, width - margin.right]);
    const yScale = d3.scaleLinear().domain(yExtent).range([height - margin.bottom, margin.top]);

    // Tooltip
    const tooltip = d3.select("body").append("div")
      .attr("class", "absolute hidden bg-slate-900 text-white p-2 rounded text-xs pointer-events-none max-w-xs shadow-xl z-50")
      .style("opacity", 0.9);

    // Dynamic keyword color scale
    const allKeywords = Array.from(new Set(data.flatMap(d => d.keywords.map(k => k.word))));
    const keywordColorScale = d3.scaleOrdinal<string, string>()
      .domain(allKeywords)
      .range(allKeywords.length <= 10
        ? d3.schemeTableau10
        : allKeywords.map((_, i) => d3.interpolateRainbow(i / allKeywords.length))
      );

    // Zoom
    const g = svg.append("g");
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 8])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
    svg.call(zoom as any);

    // Draw points
    g.selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
      .attr("cx", d => xScale(d.x))
      .attr("cy", d => yScale(d.y))
      .attr("r", 5)
      .attr("fill", d => {
        if (!d.keywords.length) return "#9ca3af"; // fallback color
        const topKeyword = d.keywords.reduce((a, b) => a.score > b.score ? a : b).keyword;
        return keywordColorScale(topKeyword);
      })
      .attr("opacity", 0.6)
      .attr("stroke", "#ffffff")
      .attr("stroke-width", 1)
      .on("mouseover", (event, d) => {
        d3.select(event.currentTarget)
          .attr("r", 8)
          .attr("opacity", 1);

        tooltip.classed("hidden", false)
          .html(formatTooltip(d))
          .style("left", (event.pageX + 10) + "px")
          .style("top", (event.pageY - 10) + "px");
      })
      .on("mouseout", (event) => {
        d3.select(event.currentTarget)
          .attr("r", 5)
          .attr("opacity", 0.6);

        tooltip.classed("hidden", true);
      });

    return () => {
      tooltip.remove();
    };
  }, [data]);

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      <h3 className="text-lg font-bold mb-4 text-slate-800">Content Projection (Semantic Map)</h3>
      <div className="bg-slate-50 rounded-xl cursor-move border border-slate-100 overflow-hidden">
        <svg 
          ref={svgRef} 
          viewBox="0 0 800 400" 
          className="w-full h-auto max-h-[500px]"
        />
      </div>
      <p className="mt-3 text-xs text-slate-400 text-center italic">
        Scroll to zoom, drag to pan. Each dot represents a post positioned by semantic similarity.
      </p>
    </div>
  );
};


export const WordCloud: React.FC<{ data: WordCloudItem[] }> = ({ data }) => {
  if (!data || data.length === 0) return null;
  
  const sortedData = [...data].sort((a, b) => b.size - a.size).slice(0, 40);
  const max = Math.max(...sortedData.map(d => d.size));
  const min = Math.min(...sortedData.map(d => d.size));

  const getSizeClass = (size: number) => {
    const scale = (size - min) / (max - min);
    if (scale > 0.8) return 'text-4xl font-black text-blue-700';
    if (scale > 0.6) return 'text-2xl font-bold text-blue-600';
    if (scale > 0.4) return 'text-xl font-semibold text-blue-500';
    if (scale > 0.2) return 'text-lg font-medium text-slate-600';
    return 'text-sm font-normal text-slate-400';
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <h3 className="text-lg font-bold mb-6 text-slate-800">Topic Cloud</h3>
      <div className="flex flex-wrap gap-x-4 gap-y-2 justify-center items-center py-8">
        {sortedData.map((item, i) => (
          <span 
            key={i} 
            className={`${getSizeClass(item.size)} hover:scale-110 transition-transform cursor-default inline-block px-1`}
            title={`${item.text}: ${item.size} occurrences`}
          >
            {item.text}
          </span>
        ))}
      </div>
    </div>
  );
};
